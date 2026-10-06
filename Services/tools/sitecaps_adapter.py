"""Offline SiteCaps 0.3.98 <-> RDF adapter. Never calls or mutates a server.

Scalar properties are editable RDF. JSON-valued fields remain lossless rdf:JSON.
Typed maintenance intervals are a checked projection of downtimeJSON.
"""
import argparse
import copy
import json
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid5, NAMESPACE_URL

from jsonschema import Draft202012Validator, FormatChecker
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD
from build_model import ROOT, SV, CONTEXT

CONTRACT = json.loads((ROOT/'sitecaps/vendor/openapi-0.3.98.json').read_text())
SCALARS = {
 'id':'siteCapsId', 'type':'siteCapsType', 'name':'name', 'version':'version',
 'prefix':'prefix', 'host':'host', 'port':'port', 'path':'path',
 'is_force_disabled':'isForceDisabled', 'is_mandatory':'isMandatory',
 'associated_compute_id':'associatedComputeId',
 'associated_storage_area_id':'associatedStorageAreaId',
}
PARENTS = {'parent_node_name':'parentNodeName', 'parent_site_name':'parentSiteName',
           'parent_site_id':'parentSiteId', 'parent_compute_id':'parentComputeId'}
JSON_FIELDS = {'other_attributes':'otherAttributes', 'downtime':'downtimeJSON'}
BOOLS = {'is_force_disabled','is_mandatory'}

def validate_service(data, scope):
    if scope not in ('local','global'): raise ValueError('scope must be local or global')
    if not isinstance(data,dict): raise ValueError('Expected a single service object')
    if 'scope' in data and data['scope'] != scope: raise ValueError('Conflicting scope')
    name = ('Local' if scope=='local' else 'Global')+'Service'
    if any(k in data for k in PARENTS): name += 'WithParentsAndType'
    schema = {'$ref':'#/components/schemas/'+name, 'components':CONTRACT['components']}
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(data)
    if scope=='global' and 'is_mandatory' in data:
        raise ValueError('is_mandatory is local-only in this profile')
    if 'id' not in data: raise ValueError('Adapter requires a registered service UUID')
    UUID(data['id'])

def parse_range(text):
    parts=text.split(' to ')
    if len(parts)!=2: raise ValueError('date_range must contain two ISO timestamps separated by " to "')
    dates=[datetime.fromisoformat(x.replace('Z','+00:00')) for x in parts]
    if any(x.tzinfo is None for x in dates): raise ValueError('Downtime timestamps need UTC/offset')
    if dates[0]>=dates[1]: raise ValueError('Downtime end must be after start')
    return parts

def maintenance_projection(g, subject, downtime):
    for i,item in enumerate(downtime):
        start,end=parse_range(item['date_range'])
        m=URIRef(str(subject)+'/downtime/'+str(i))
        g.add((subject,SV.maintenance,m)); g.add((m,RDF.type,SV.MaintenanceWindow))
        for p,v,dt in [('startsAt',start,XSD.dateTime),('endsAt',end,XSD.dateTime),
                       ('downtimeKind',item['type'],None),('reason',item['reason'],None)]:
            g.add((m,SV[p],Literal(v,datatype=dt)))

def import_service(data, scope, registry):
    """Import a service read object; registry origin namespaces UUID identity."""
    validate_service(data,scope)
    if not registry.startswith(('https://','http://')): raise ValueError('registry must be an absolute HTTP(S) API base')
    identity=str(uuid5(NAMESPACE_URL,registry.rstrip('/')+'|'+data['id']))
    subject=URIRef('urn:srcnet:sitecaps:'+identity)
    g=Graph()
    for prefix,iri in CONTEXT.items(): g.bind(prefix,iri)
    g.add((subject,RDF.type,SV.SiteCapsRecord)); g.add((subject,SV.scope,Literal(scope)))
    g.add((subject,SV.contractVersion,Literal('0.3.98')))
    # Scope may be supplied externally for a nested LocalService/GlobalService.
    for key,p in SCALARS.items():
        if key in data: g.add((subject,SV[p],Literal(data[key])))
    for key,p in JSON_FIELDS.items():
        g.add((subject,SV[p],Literal(json.dumps(data[key],sort_keys=True),datatype=RDF.JSON)))
    extras={k:v for k,v in data.items() if k not in SCALARS and k not in JSON_FIELDS and k not in PARENTS}
    # Includes presence/absence of scope; prevents adding fields on a round trip.
    g.add((subject,SV.extraFields,Literal(json.dumps(extras,sort_keys=True),datatype=RDF.JSON)))
    if any(k in data for k in PARENTS):
        ctx=URIRef(str(subject)+'/parents'); g.add((subject,SV.registrationContext,ctx))
        g.add((ctx,RDF.type,SV.RegistrationContext))
        for key,p in PARENTS.items():
            if key in data: g.add((ctx,SV[p],Literal(data[key])))
    maintenance_projection(g,subject,data['downtime'])
    return g

def one(g,s,p,required=True):
    values=list(g.objects(s,p))
    if len(values)>1 or (required and not values): raise ValueError(f'Expected one value of {p}')
    return values[0] if values else None

def export_service(g):
    subjects=list(g.subjects(RDF.type,SV.SiteCapsRecord))
    if len(subjects)!=1: raise ValueError('Export requires exactly one SiteCapsRecord')
    s=subjects[0]; scope=str(one(g,s,SV.scope))
    if str(one(g,s,SV.contractVersion))!='0.3.98': raise ValueError('Unsupported contract version')
    data=json.loads(str(one(g,s,SV.extraFields)))
    if not isinstance(data,dict): raise ValueError('extraFields must be an object')
    if any(k in data for k in {*SCALARS,*PARENTS,*JSON_FIELDS}): raise ValueError('Extra fields collide with mapped fields')
    if 'scope' in data: data['scope']=scope
    for key,p in SCALARS.items():
        v=one(g,s,SV[p],False)
        if v is not None:
            if key in BOOLS:
                if v.datatype!=XSD.boolean or type(v.toPython()) is not bool: raise ValueError('Expected RDF boolean')
                data[key]=v.toPython()
            elif key=='port':
                if v.datatype!=XSD.integer or type(v.toPython()) is not int: raise ValueError('Expected RDF integer port')
                data[key]=v.toPython()
            else:
                if not isinstance(v,Literal) or v.datatype not in (None,XSD.string): raise ValueError('Expected string literal')
                data[key]=str(v)
    for key,p in JSON_FIELDS.items():
        v=one(g,s,SV[p])
        if v.datatype!=RDF.JSON: raise ValueError('Expected rdf:JSON')
        data[key]=json.loads(str(v))
    ctx=one(g,s,SV.registrationContext,False)
    if ctx is not None:
        for key,p in PARENTS.items():
            v=one(g,ctx,SV[p],False)
            if v is not None: data[key]=str(v)
    validate_service(data,scope)
    expected=Graph(); maintenance_projection(expected,s,data['downtime'])
    # Reject conflicting edits instead of silently exporting stale downtime JSON.
    actual=set()
    for m in g.objects(s,SV.maintenance):
        actual.add((s,SV.maintenance,m))
        actual.update((m,p,o) for p,o in g.predicate_objects(m)
                      if p in (RDF.type,SV.startsAt,SV.endsAt,SV.downtimeKind,SV.reason))
    if actual!=set(expected): raise ValueError('Maintenance projection differs from downtimeJSON; regenerate the projection')
    return data

def nest_in_node(node, service, scope, compute_id):
    """Copy a full node and replace one existing registered service; no network I/O.

    No implicit create, no removal of sibling records, no UUID regeneration.
    Parent fields are discovery metadata and are excluded from nested objects.
    """
    validate_service(service,scope)
    result=copy.deepcopy(node)
    matches=[c for site in result.get('sites',[]) for c in site.get('compute',[]) if c.get('id')==compute_id]
    if len(matches)!=1: raise ValueError('Expected exactly one existing compute resource')
    target=matches[0]
    if 'parent_compute_id' in service and service['parent_compute_id']!=compute_id:
        raise ValueError('Parent compute mismatch')
    parent_site=next(site for site in result['sites'] if any(c is target for c in site.get('compute',[])))
    checks={'parent_node_name':result.get('name'),'parent_site_name':parent_site.get('name'),'parent_site_id':parent_site.get('id')}
    for key,value in checks.items():
        if key in service and service[key]!=value: raise ValueError(f'Parent mismatch: {key}')
    key='associated_'+scope+'_services'
    records=target.get(key,[])
    indexes=[i for i,r in enumerate(records) if r.get('id')==service['id']]
    if len(indexes)!=1: raise ValueError('Expected exactly one existing service in the selected scope')
    records[indexes[0]]={k:v for k,v in service.items() if k not in PARENTS and k!='scope'}
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    imp=sub.add_parser('import'); imp.add_argument('input'); imp.add_argument('output')
    imp.add_argument('--scope',required=True,choices=['local','global'])
    imp.add_argument('--registry',required=True)
    exp=sub.add_parser('export'); exp.add_argument('input'); exp.add_argument('output')
    args=p.parse_args()
    if args.command=='import':
        g=import_service(json.loads(Path(args.input).read_text()),args.scope,args.registry)
        fmt='turtle' if args.output.endswith('.ttl') else 'json-ld'
        options={'context':CONTEXT,'indent':2} if fmt=='json-ld' else {}
        g.serialize(args.output,format=fmt,**options)
    else:
        fmt='turtle' if args.input.endswith('.ttl') else 'json-ld'
        result=export_service(Graph().parse(args.input,format=fmt))
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__': main()
