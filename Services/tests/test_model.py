import copy
import json
import sys
from pathlib import Path

import pytest
from jsonschema import ValidationError
from pyshacl import validate
from rdflib import Graph, URIRef, Literal
from rdflib.compare import isomorphic
from rdflib.namespace import RDF, XSD, OWL

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_model import SV
from sitecaps_adapter import import_service, export_service, nest_in_node, CONTRACT

def fixture(scope='local'):
    return json.loads((ROOT/f'examples/sitecaps-{scope}.synthetic.json').read_text())

@pytest.mark.parametrize('stem',['ontology/services','examples/espsrc-services','examples/synthetic-performance',
                                 'examples/global-service-template','examples/sitecaps-local.synthetic','examples/sitecaps-global.synthetic'])
def test_serializations_are_same_rdf(stem):
    assert isomorphic(Graph().parse(ROOT/(stem+'.ttl')),Graph().parse(ROOT/(stem+'.jsonld'),format='json-ld'))

@pytest.mark.parametrize('filename',['espsrc-services.ttl','synthetic-performance.ttl','global-service-template.ttl',
                                     'sitecaps-local.synthetic.jsonld','sitecaps-global.synthetic.ttl'])
def test_shapes(filename):
    g=Graph().parse(ROOT/'examples'/filename,format='json-ld' if filename.endswith('jsonld') else 'turtle')
    ok,_,report=validate(g,shacl_graph=str(ROOT/'ontology/shapes.ttl'),ont_graph=str(ROOT/'ontology/services.ttl'))
    assert ok,report

@pytest.mark.parametrize('scope',['local','global'])
@pytest.mark.parametrize('fmt',['turtle','json-ld'])
def test_roundtrip(scope,fmt):
    d=fixture(scope)
    g=import_service(d,scope,'https://sitecaps.example.org/api/v1')
    g=Graph().parse(data=g.serialize(format=fmt),format=fmt)
    assert export_service(g)==d

@pytest.mark.parametrize('scope,type_name',[(scope,t) for scope,key in [('local','LocalService'),('global','GlobalService')]
                         for t in CONTRACT['components']['schemas'][key]['properties']['type']['enum']])
def test_every_advertised_type(scope,type_name):
    d=fixture(scope); d['type']=type_name
    assert export_service(import_service(d,scope,'https://example.org'))==d

@pytest.mark.parametrize('change',[{'id':'not-a-uuid'},{'is_force_disabled':'false'},
                                  {'port':443.5},{'type':'science-gateway'},
                                  {'scope':'global'},{'host':None}])
def test_invalid_contract_rejected(change):
    d=fixture(); d.update(change)
    with pytest.raises((ValidationError,ValueError)): import_service(d,'local','https://example.org')

def test_absent_optional_fields_preserved():
    d=fixture()
    for k in list(d):
        if k.startswith('parent_') or k in ('scope','associated_compute_id','associated_storage_area_id'): del d[k]
    assert export_service(import_service(d,'local','https://example.org'))==d

def test_different_registries_do_not_merge_ids():
    a=import_service(fixture(),'local','https://one.example.org')
    b=import_service(fixture(),'local','https://two.example.org')
    assert set(a.subjects(RDF.type,SV.SiteCapsRecord)).isdisjoint(b.subjects(RDF.type,SV.SiteCapsRecord))

def test_graph_edit_changes_flag_without_claiming_health():
    g=import_service(fixture(),'local','https://example.org')
    s=next(g.subjects(RDF.type,SV.SiteCapsRecord)); g.set((s,SV.isForceDisabled,Literal(True)))
    assert export_service(g)['is_force_disabled'] is True
    assert not list(g.triples((None,SV.health,None)))

def test_duplicate_scalar_rejected():
    g=import_service(fixture(),'local','https://example.org')
    s=next(g.subjects(RDF.type,SV.SiteCapsRecord)); g.add((s,SV.port,Literal(8443)))
    with pytest.raises(ValueError): export_service(g)

def test_downtime_projection_conflict_rejected():
    g=import_service(fixture(),'local','https://example.org')
    m=next(g.subjects(RDF.type,SV.MaintenanceWindow)); g.set((m,SV.reason,Literal('Changed only RDF projection')))
    with pytest.raises(ValueError,match='projection'): export_service(g)

@pytest.mark.parametrize('date_range',['2026-10-10 to 2026-10-11','2026-10-11T00:00:00Z to 2026-10-10T00:00:00Z','nonsense'])
def test_bad_downtime_rejected(date_range):
    d=fixture(); d['downtime'][0]['date_range']=date_range
    with pytest.raises(ValueError): import_service(d,'local','https://example.org')

def test_nested_update_preserves_siblings_and_context():
    d=fixture(); old={k:v for k,v in d.items() if not k.startswith('parent_') and k!='scope'}
    sibling={'id':'unchanged','other_attributes':{'important':True}}
    node={'name':'EXAMPLE','version':7,'untouched':{'x':1},'sites':[{'id':d['parent_site_id'],'name':'EXAMPLE-SITE','compute':[
        {'id':d['parent_compute_id'],'associated_local_services':[old,sibling],'queues':[{'keep':True}]}]}]}
    before=copy.deepcopy(node); d['is_force_disabled']=True
    result=nest_in_node(node,d,'local',d['parent_compute_id'])
    assert node==before
    services=result['sites'][0]['compute'][0]['associated_local_services']
    assert services[0]['is_force_disabled'] is True
    assert services[1]==sibling
    assert 'scope' not in services[0] and 'parent_compute_id' not in services[0]
    assert result['sites'][0]['compute'][0]['queues']==[{'keep':True}]
    assert result['version']==7
    d['parent_node_name']='WRONG'
    with pytest.raises(ValueError,match='Parent mismatch'): nest_in_node(node,d,'local',d['parent_compute_id'])

def test_bad_quantity_fails_shacl():
    g=Graph().parse(ROOT/'examples/synthetic-performance.ttl')
    unit=URIRef('http://qudt.org/schema/qudt/unit')
    g.remove((None,unit,None))
    ok,_,_=validate(g,shacl_graph=str(ROOT/'ontology/shapes.ttl'))
    assert not ok

def test_legacy_identity_links():
    g=Graph().parse(ROOT/'examples/espsrc-services.ttl')
    for key in ['espsrc-notebook','espsrcscienceplatform','espsrcsoda','espsrc-datalake','authentication','sciencegateway','datadistributionplatform','registryservice']:
        assert (URIRef('https://w3id.org/srcnet/service/'+key),RDF.type,SV.Service) in g
    assert not list(g.subjects(RDF.type,SV.SiteCapsRecord)) # No invented real UUIDs.
    assert not list(g.triples((None,SV.health,Literal('up'))))

def test_all_extension_predicates_declared():
    ont=Graph().parse(ROOT/'ontology/services.ttl')
    for path in (ROOT/'examples').glob('*.ttl'):
        g=Graph().parse(path)
        for p in set(g.predicates()):
            if str(p).startswith(str(SV)):
                assert (p,RDF.type,OWL.ObjectProperty) in ont or (p,RDF.type,OWL.DatatypeProperty) in ont,p

def test_live_type_snapshot_matches_contract():
    types=json.loads((ROOT/'sitecaps/vendor/services-types-0.3.98.json').read_text())
    for scope,key in [('local','LocalService'),('global','GlobalService')]:
        assert types[scope]==CONTRACT['components']['schemas'][key]['properties']['type']['enum']

@pytest.mark.parametrize('scope',['local','global'])
def test_committed_enriched_registration_exports(scope):
    g=Graph().parse(ROOT/f'examples/sitecaps-{scope}.synthetic.ttl')
    assert export_service(g)==fixture(scope)
    assert len(list(g.triples((None,SV.registration,None))))==1

@pytest.mark.parametrize('query,example,nonempty',[
    ('local-services','espsrc-services',True),('dependencies','espsrc-services',True),
    ('legacy-catalog','espsrc-services',True),('performance','synthetic-performance',True),
    ('disabled-registrations','sitecaps-local.synthetic',False)])
def test_competency_queries(query,example,nonempty):
    g=Graph().parse(ROOT/f'examples/{example}.ttl')
    rows=list(g.query((ROOT/f'queries/{query}.rq').read_text()))
    assert bool(rows) is nonempty
