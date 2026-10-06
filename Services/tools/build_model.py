"""Generate the vocabulary and examples deterministically; no network access."""
import json
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, DCTERMS

ROOT = Path(__file__).resolve().parents[1]
SV = Namespace('https://w3id.org/srcnet/services#')
SRC = Namespace('https://w3id.org/srcnet#')
SCHEMA = Namespace('https://schema.org/')
DCAT = Namespace('http://www.w3.org/ns/dcat#')
PROV = Namespace('http://www.w3.org/ns/prov#')
QUDT = Namespace('http://qudt.org/schema/qudt/')
CONTEXT = {'sv': str(SV), 'src': str(SRC), 'schema': str(SCHEMA),
           'dcat': str(DCAT), 'prov': str(PROV), 'qudt': str(QUDT),
           'unit': 'http://qudt.org/vocab/unit/', 'xsd': str(XSD),
           'rdf': str(RDF), 'rdfs': str(RDFS), 'owl': str(OWL), 'dcterms': str(DCTERMS)}

CLASSES = {
 'Service': 'Stable logical service, reusing the original catalogue identity.',
 'Deployment': 'A service deployed in one environment. Separate from a SiteCaps registration.',
 'Site': 'Physical or administrative site within a SRC node; explicit SiteCaps site level.',
 'OperationalProfile': 'Lifecycle, observed health, monitoring and maintenance information.',
 'FunctionalProfile': 'Functions, standards, interfaces and supported data formats.',
 'AdministrationProfile': 'Accountable operator, support, escalation, runbooks and change management.',
 'SecurityProfile': 'Authentication and authorisation policy references; never credentials.',
 'ResourceAllocation': 'Service allocation or request over a shared infrastructure resource.',
 'InfrastructureResource': 'Compute, storage or network resource used by a deployment.',
 'SoftwareRelease': 'Version of one software component; chart and application are distinct.',
 'Endpoint': 'An interface URL with a role, protocol and evidence status.',
 'Dependency': 'Directed dependency of a deployment on a logical service.',
 'Measurement': 'Timestamped metric with value, unit, method and evidence.',
 'ServiceObjective': 'Target with a comparator and evaluation window; not a measurement.',
 'MaintenanceWindow': 'Planned or unplanned downtime interval.',
 'Evidence': 'Source and date of a report, observation, proposal or synthetic fixture.',
 'SiteCapsRecord': 'Version-bound projection of a SiteCaps local/global service object.',
 'RegistrationContext': 'Parent node/site/compute identifiers returned by SiteCaps.',
}
# No global domains: shared predicates must not infer unintended class membership.
OBJECTS = {
 'hasDeployment': ('Deployment', 'Links a logical service to a deployment.'),
 'realizesService': ('Service', 'Logical service implemented by this deployment.'),
 'hostedAt': ('Site', 'Actual hosting site; global scope does not imply hosting at every consumer.'),
 'partOfNode': (str(SRC.Node), 'Node containing this site.'),
 'operational': ('OperationalProfile', 'Operational description.'),
 'functional': ('FunctionalProfile', 'Functional description.'),
 'administration': ('AdministrationProfile', 'Administration description.'),
 'security': ('SecurityProfile', 'Security description.'),
 'allocation': ('ResourceAllocation', 'Allocation, requirement or quota; not whole-site capacity.'),
 'resource': ('InfrastructureResource', 'Shared resource to which an allocation applies.'),
 'software': ('SoftwareRelease', 'Component release.'),
 'endpoint': ('Endpoint', 'Service interface.'),
 'dependency': ('Dependency', 'Dependency assertion with evidence.'),
 'targetService': ('Service', 'Logical dependency target.'),
 'measurement': ('Measurement', 'An observed performance value.'),
 'objective': ('ServiceObjective', 'A proposed or agreed target.'),
 'maintenance': ('MaintenanceWindow', 'A maintenance interval.'),
 'evidence': ('Evidence', 'Evidence supporting this entity description.'),
 'registration': ('SiteCapsRecord', 'External SiteCaps projection.'),
 'registrationContext': ('RegistrationContext', 'Discovery parent metadata, not deployment ownership.'),
 'operator': (str(SCHEMA.Organization), 'Accountable operating organisation.'),
 'authenticatesWith': ('Service', 'Authentication service consumed by this service.'),
 'consumesService': ('Service', 'Consumption without claiming local hosting.'),
 'quantity': (str(QUDT.QuantityValue), 'Measured, requested or allocated quantity.'),
}
DATA = {
 'scope': ('string', 'local or global logical service scope; independent of physical hosting.'),
 'serviceKind': ('string', 'Open semantic classification; not the SiteCaps type enumeration.'),
 'environment': ('string', 'Deployment environment: production, preproduction, test or example.'),
 'lifecycle': ('string', 'reported-deployed, planned, retired or unknown.'),
 'health': ('string', 'up, degraded, down or unknown; never inferred from the force-disable flag.'),
 'evidenceStatus': ('string', 'reported, observed, proposed or synthetic.'),
 'sourceDate': ('date', 'Date of the source information, not a live availability assertion.'),
 'function': ('string', 'Function provided, independently of implementation.'),
 'format': ('string', 'Supported data format or MIME type.'),
 'protocol': ('string', 'Interface or authentication protocol.'),
 'endpointRole': ('string', 'Role such as portal, API, capabilities, health or metrics.'),
 'namespace': ('string', 'Kubernetes namespace.'),
 'workloadNamespace': ('string', 'Namespace for user workload pods.'),
 'orchestrator': ('string', 'Deployment orchestration technology.'),
 'releaseKind': ('string', 'application, helm-chart or container-image.'),
 'version': ('string', 'Version of the identified component.'),
 'releaseName': ('string', 'Helm release identifier.'),
 'repository': ('anyURI', 'Source repository URL.'),
 'runbook': ('anyURI', 'Operator runbook URL.'),
 'supportURL': ('anyURI', 'Support entry point.'),
 'escalation': ('string', 'Escalation route or responsible team.'),
 'changeManagement': ('string', 'Mechanism for reviewing and applying changes.'),
 'backupPolicy': ('string', 'Backup policy reference or description.'),
 'authorizationPolicy': ('anyURI', 'Authorisation policy reference.'),
 'tokenAudience': ('string', 'Expected token audience; not a token.'),
 'tokenScope': ('string', 'Expected OAuth scope.'),
 'allocationKind': ('string', 'request, limit, quota or allocated; do not add shared capacities.'),
 'resourceKind': ('string', 'compute, storage or network.'),
 'storageClass': ('string', 'Kubernetes storage class.'),
 'claimName': ('string', 'PVC claim name; namespace must also be supplied.'),
 'metric': ('string', 'Metric name, e.g. latency-p95, throughput or cpu-cores.'),
 'method': ('string', 'Measurement method and aggregation definition.'),
 'window': ('duration', 'Measurement or objective evaluation window.'),
 'comparator': ('string', 'Objective comparator: <=, >= or =.'),
 'dependencyKind': ('string', 'hard or soft dependency.'),
 'startsAt': ('dateTime', 'UTC or offset-aware interval start.'),
 'endsAt': ('dateTime', 'UTC or offset-aware interval end.'),
 'downtimeKind': ('string', 'Planned or Unplanned, matching SiteCaps.'),
 'reason': ('string', 'Maintenance reason.'),
 'siteCapsId': ('string', 'SiteCaps service UUID; never fabricated for a real deployment.'),
 'siteCapsType': ('string', 'Exact SiteCaps type from the pinned scope enumeration.'),
 'name': ('string', 'Name in the SiteCaps object.'),
 'prefix': ('string', 'SiteCaps URL scheme without separators.'),
 'host': ('string', 'SiteCaps host, preserved verbatim.'),
 'port': ('integer', 'SiteCaps port, preserved verbatim.'),
 'path': ('string', 'SiteCaps endpoint path, preserved verbatim.'),
 'isForceDisabled': ('boolean', 'SiteCaps administrative force-disable flag.'),
 'isMandatory': ('boolean', 'SiteCaps local-service mandatory flag.'),
 'associatedComputeId': ('string', 'Associated compute UUID, distinct from parent_compute_id.'),
 'associatedStorageAreaId': ('string', 'Associated storage area UUID.'),
 'parentNodeName': ('string', 'SiteCaps parent_node_name; do not guess from a display label.'),
 'parentSiteName': ('string', 'SiteCaps parent_site_name.'),
 'parentSiteId': ('string', 'SiteCaps parent_site_id UUID.'),
 'parentComputeId': ('string', 'SiteCaps parent_compute_id UUID.'),
 'contractVersion': ('string', 'SiteCaps contract version against which the record was checked.'),
 'otherAttributes': (str(RDF.JSON), 'Lossless SiteCaps extensibility JSON; semantic detail may be linked here.'),
 'downtimeJSON': (str(RDF.JSON), 'Lossless original downtime array, including order and extension fields.'),
 'extraFields': (str(RDF.JSON), 'Unrecognised fields retained without inventing semantic meaning.'),
}

def write_graph(g, stem):
    for prefix, iri in CONTEXT.items(): g.bind(prefix, Namespace(iri))
    (ROOT / (stem + '.ttl')).write_text(g.serialize(format='turtle').rstrip()+'\n')
    g.serialize(ROOT / (stem + '.jsonld'), format='json-ld', context=CONTEXT, indent=2)

def vocabulary():
    g = Graph()
    ont = URIRef(str(SV).rstrip('#'))
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, OWL.versionInfo, Literal('0.1.0')))
    g.add((ont, RDFS.comment, Literal('Proposed SRCNet services extension. Namespace is not registered or endorsed. No remote imports required.')))
    for name, desc in CLASSES.items():
        g.add((SV[name], RDF.type, OWL.Class)); g.add((SV[name], RDFS.label, Literal(name)))
        g.add((SV[name], RDFS.comment, Literal(desc)))
    g.add((SV.Service, RDFS.subClassOf, DCAT.DataService))
    g.add((SV.InfrastructureResource, RDFS.subClassOf, PROV.Entity))
    for name, (rng, desc) in OBJECTS.items():
        g.add((SV[name], RDF.type, OWL.ObjectProperty))
        g.add((SV[name], RDFS.range, URIRef(rng) if ':' in rng else SV[rng]))
        g.add((SV[name], RDFS.comment, Literal(desc)))
    for name, (rng, desc) in DATA.items():
        g.add((SV[name], RDF.type, OWL.DatatypeProperty))
        g.add((SV[name], RDFS.range, URIRef(rng) if ':' in rng else XSD[rng]))
        g.add((SV[name], RDFS.comment, Literal(desc)))
    write_graph(g, 'ontology/services')
    (ROOT/'ontology/context.jsonld').write_text(json.dumps({'@context': CONTEXT}, indent=2)+'\n')
    rows = ['# Vocabulary reference', '', 'Proposed namespace: `https://w3id.org/srcnet/services#`.', '',
            '## Classes', '', '| Term | Meaning |', '|---|---|']
    rows += [f'| `sv:{k}` | {v} |' for k,v in CLASSES.items()]
    rows += ['', '## Properties', '', '| Term | Range | Meaning |', '|---|---|---|']
    rows += [f'| `sv:{k}` | `{v[0]}` | {v[1]} |' for k,v in {**OBJECTS, **DATA}.items()]
    (ROOT/'docs/vocabulary.md').write_text('\n'.join(rows)+'\n')

def examples():
    g = Graph()
    base = 'https://example.org/srcnet/espSRC/'
    def node(name, cls, label=None):
        u = URIRef(base+name); g.add((u,RDF.type,SV[cls]))
        if label: g.add((u,SCHEMA.name,Literal(label)))
        return u
    def val(s,p,v,datatype=None): g.add((s,SV[p],Literal(v,datatype=datatype)))
    def link(s,p,o): g.add((s,SV[p],o))
    evidence = node('evidence/operator-report-2026-10-02','Evidence','Operator configuration reports, 29 September–2 October 2026')
    val(evidence,'sourceDate','2026-10-02',XSD.date); val(evidence,'evidenceStatus','reported')
    g.add((evidence,SCHEMA.description,Literal('User-provided configuration history. Not a live probe or a SiteCaps database extract. Includes Skaha chart 1.7.0 / application 1.4.0 and CANFAR component deployment.')))
    proposal = node('evidence/design','Evidence','Architectural interpretation for this example')
    val(proposal,'sourceDate','2026-10-06',XSD.date); val(proposal,'evidenceStatus','proposed')
    srcnode=URIRef('https://w3id.org/srcnet/node/espsrc-node')
    g.add((srcnode,RDF.type,SRC.Node))
    org=URIRef('https://w3id.org/srcnet/node/espsrc')
    g.add((org,RDF.type,SRC.SRC)); g.add((org,DCTERMS.hasPart,srcnode))
    site=node('site/iaa','Site','IAA-CSIC espSRC site')
    link(site,'partOfNode',srcnode); link(site,'evidence',evidence)
    operator=URIRef(base+'organization/iaa-csic')
    g.add((operator,RDF.type,SCHEMA.Organization)); g.add((operator,SCHEMA.name,Literal('IAA-CSIC espSRC')))
    local=URIRef('https://w3id.org/srcnet/catalog/espsrc-local')
    globalcat=URIRef('https://w3id.org/srcnet/catalog/srcnet-global')
    for cat,p in [(local,SRC.localServiceCatalog),(globalcat,SRC.globalServiceCatalog)]:
        g.add((cat,RDF.type,DCAT.Catalog)); g.add((srcnode,p,cat))
    resource=node('resource/k3s-production','InfrastructureResource','espSRC production k3s cluster on OpenStack')
    val(resource,'resourceKind','compute'); val(resource,'orchestrator','k3s / Kubernetes'); link(resource,'evidence',evidence)
    storage=node('resource/cephfs','InfrastructureResource','Shared CephFS storage')
    val(storage,'resourceKind','storage'); link(storage,'evidence',evidence)
    # Old service IDs are retained. New implementation components get separate IDs.
    services = [
      ('espsrcscienceplatform','CANFAR science platform','canfar','local','Interactive science sessions','skaha-system'),
      ('espsrc-notebook','Notebook capability through CANFAR','notebook','local','Interactive notebook execution',None),
      ('espsrcsoda','SODA data access','soda','local','Server-side data access','espsrcsoda'),
      ('espsrc-datalake','espSRC data lake / Rucio storage','datalake','local','Local data storage and access',None),
      ('espsrc-skaha','Skaha session service','skaha','local','Create and manage user sessions','skaha-system'),
      ('espsrc-cavern','Cavern storage service','cavern','local','User file access','skaha-system'),
      ('espsrc-posixmapper','PosixMapper','posix-mapper','local','Map identities to POSIX users and groups','skaha-system'),
      ('espsrc-preparedata','PrepareData','prepare_data','local','Stage data for execution','preparedata'),
      ('espsrc-gatekeeper','Gatekeeper','gatekeeper','local','Authorise service requests',None),
      ('authentication','SRCNet IAM','iam','global','Federated authentication',None),
      ('sciencegateway','SRCNet Science Gateway','science-gateway','global','Unified science entry point',None),
      ('datadistributionplatform','SRCNet data distribution','data-distribution','global','Federated data management',None),
      ('registryservice','SRCNet registry','registry','global','Service and resource discovery',None),
    ]
    ids={}; deployments={}
    for key,label,kind,scope,function,ns in services:
        s=URIRef('https://w3id.org/srcnet/service/'+key); ids[key]=s
        g.add((s,RDF.type,SV.Service)); g.add((s,RDF.type,DCAT.DataService))
        g.add((s,SCHEMA.name,Literal(label))); val(s,'scope',scope); val(s,'serviceKind',kind)
        g.add(((local if scope=='local' else globalcat),DCAT.service,s))
        f=node('function/'+key,'FunctionalProfile'); link(s,'functional',f); val(f,'function',function); link(f,'evidence',proposal)
        link(s,'evidence', evidence if scope=='local' or key=='authentication' else proposal)
        if scope=='global':
            link(srcnode,'consumesService',s)
            # Hosting, release and deployment state of global services are unknown.
            continue
        # Notebook is a capability implemented by Skaha, not another deployed JupyterHub.
        if key=='espsrc-notebook': continue
        d=node('deployment/'+key+'/production','Deployment',label+' deployment')
        deployments[key]=d; link(s,'hasDeployment',d); link(d,'realizesService',s)
        val(d,'environment','production'); link(d,'hostedAt',site); link(d,'evidence',evidence)
        op=node('operational/'+key,'OperationalProfile'); link(d,'operational',op)
        val(op,'lifecycle','reported-deployed'); val(op,'health','unknown'); link(op,'evidence',evidence)
        adm=node('administration/'+key,'AdministrationProfile'); link(d,'administration',adm)
        link(adm,'operator',operator); link(adm,'evidence',evidence)
        if ns:
            val(d,'namespace',ns); val(adm,'changeManagement','Flux GitOps / Helm')
        if key not in ['espsrc-datalake']:
            allocation=node('allocation/'+key,'ResourceAllocation'); link(d,'allocation',allocation)
            link(allocation,'resource',resource); val(allocation,'allocationKind','allocated'); link(allocation,'evidence',evidence)
            # No CPU/RAM/GPU totals invented; lack of quantity means unknown.
    def dependency(key,target,kind='hard'):
        dep=node('dependency/'+key+'/'+target,'Dependency'); link(deployments[key],'dependency',dep)
        link(dep,'targetService',ids[target]); val(dep,'dependencyKind',kind); link(dep,'evidence',proposal)
    dependency('espsrcscienceplatform','espsrc-skaha')
    dependency('espsrc-skaha','authentication'); dependency('espsrc-skaha','espsrc-cavern')
    dependency('espsrc-cavern','espsrc-posixmapper')
    dependency('espsrc-preparedata','espsrc-datalake')
    dependency('espsrcsoda','espsrc-datalake')
    for key in ['espsrc-datalake','espsrc-skaha','espsrc-cavern']:
        a=node('storage-allocation/'+key,'ResourceAllocation'); link(deployments[key],'allocation',a)
        link(a,'resource',storage); val(a,'allocationKind','allocated'); link(a,'evidence',evidence)
    link(ids['espsrc-notebook'],'hasDeployment',deployments['espsrc-skaha'])
    link(deployments['espsrc-skaha'],'realizesService',ids['espsrc-notebook'])
    for key,url,role in [
      ('espsrcscienceplatform','https://canfar.espsrc.iaa.csic.es','portal'),
      ('authentication','https://ska-iam.stfc.ac.uk/','identity-provider')]:
        ep=node('endpoint/'+key,'Endpoint'); link(ids[key],'endpoint',ep)
        g.add((ep,DCAT.endpointURL,URIRef(url))); val(ep,'endpointRole',role); link(ep,'evidence',evidence)
    sk=deployments['espsrc-skaha']; val(sk,'workloadNamespace','skaha-workload')
    for name,version,kind in [('skaha','1.4.0','application'),('skaha-chart','1.7.0','helm-chart')]:
        r=node('release/'+name+'/'+version,'SoftwareRelease',name); val(r,'version',version); val(r,'releaseKind',kind)
        link(sk,'software',r); link(r,'evidence',evidence)
    val(sk,'releaseName','espsrccanfar-science-platform')
    security=node('security/canfar','SecurityProfile'); link(sk,'security',security)
    link(security,'authenticatesWith',ids['authentication']); val(security,'protocol','OIDC'); link(security,'evidence',evidence)
    g.add((sk,SCHEMA.description,Literal('Known configuration, not current health. Earlier PVC and metrics-backend incidents do not establish present availability. Chart and image versions are intentionally separate.')))
    write_graph(g,'examples/espsrc-services')

    # Independent synthetic graph exercises numeric performance and resource semantics.
    g=Graph()
    ev=node('synthetic/evidence','Evidence','Synthetic tutorial data; not espSRC measurements')
    val(ev,'evidenceStatus','synthetic'); val(ev,'sourceDate','2026-10-06',XSD.date)
    s=node('synthetic/service','Service','Example service'); val(s,'scope','local'); val(s,'serviceKind','canfar')
    d=node('synthetic/deployment','Deployment'); link(s,'hasDeployment',d); link(d,'realizesService',s)
    val(d,'environment','example'); link(d,'evidence',ev)
    for cls,key,value,unit in [('Measurement','latency-p95',0.25,'SEC'),('ServiceObjective','availability',99.5,'PERCENT')]:
        m=node('synthetic/'+key,cls); link(d,'measurement' if cls=='Measurement' else 'objective',m)
        val(m,'metric',key); val(m,'window','P30D',XSD.duration); link(m,'evidence',ev)
        q=URIRef(base+'synthetic/'+key+'/value'); link(m,'quantity',q)
        g.add((q,RDF.type,QUDT.QuantityValue)); g.add((q,QUDT.numericValue,Literal(str(value),datatype=XSD.decimal)))
        g.add((q,QUDT.unit,URIRef(CONTEXT['unit']+unit)))
        if cls=='Measurement':
            g.add((m,PROV.generatedAtTime,Literal('2026-10-06T00:00:00Z',datatype=XSD.dateTime)))
            val(m,'method','Synthetic example: p95 HTTP response latency over the stated window')
        else: val(m,'comparator','>=')
    r=node('synthetic/compute','InfrastructureResource'); val(r,'resourceKind','compute')
    a=node('synthetic/allocation','ResourceAllocation'); link(d,'allocation',a); link(a,'resource',r)
    val(a,'allocationKind','request'); val(a,'metric','memory-bytes'); link(a,'evidence',ev)
    q=URIRef(base+'synthetic/memory'); link(a,'quantity',q)
    g.add((q,RDF.type,QUDT.QuantityValue)); g.add((q,QUDT.numericValue,Literal('8589934592.0',datatype=XSD.decimal)))
    g.add((q,QUDT.unit,URIRef(CONTEXT['unit']+'BYTE')))
    write_graph(g,'examples/synthetic-performance')

def global_template():
    """A complete but deliberately fictional global-service description."""
    c=dict(CONTEXT); c['ex']='https://example.org/srcnet/global/'
    def ref(x): return {'@id':x}
    def typed(value,typ): return {'@value':value,'@type':typ}
    records=[
      {'@id':'ex:iam','@type':['sv:Service','dcat:DataService'],'schema:name':'Synthetic global IAM',
       'sv:scope':'global','sv:serviceKind':'iam','sv:hasDeployment':ref('ex:deployment'),
       'sv:functional':ref('ex:functional'),'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:deployment','@type':'sv:Deployment','sv:environment':'example',
       'sv:realizesService':ref('ex:iam'),'sv:hostedAt':ref('ex:hosting-site'),
       'sv:operational':ref('ex:operations'),'sv:administration':ref('ex:administration'),
       'sv:security':ref('ex:security'),'sv:allocation':ref('ex:allocation'),
       'sv:objective':ref('ex:objective'),'sv:endpoint':ref('ex:endpoint'),
       'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:evidence','@type':'sv:Evidence','sv:evidenceStatus':'synthetic',
       'sv:sourceDate':typed('2026-10-06','xsd:date'),
       'schema:description':'Template only. All organisations, sites, resources and targets are fictional.'},
      {'@id':'ex:hosting-site','@type':'sv:Site','schema:name':'Example IAM hosting site',
       'sv:partOfNode':ref('ex:hosting-node')},
      {'@id':'ex:hosting-node','@type':'src:Node','sv:consumesService':ref('ex:iam')},
      {'@id':'ex:consumer-node','@type':'src:Node','sv:consumesService':ref('ex:iam')},
      {'@id':'ex:functional','@type':'sv:FunctionalProfile','sv:function':['Federated authentication','Token issuance'],
       'sv:protocol':['OpenID Connect','OAuth 2.0'],'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:operations','@type':'sv:OperationalProfile','sv:lifecycle':'planned','sv:health':'unknown',
       'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:endpoint','@type':'sv:Endpoint','dcat:endpointURL':ref('https://iam.example.org/'),
       'sv:endpointRole':'identity-provider','sv:evidence':ref('ex:evidence')},
      {'@id':'ex:administration','@type':'sv:AdministrationProfile','sv:operator':ref('ex:operator'),
       'sv:supportURL':typed('https://support.example.org/','xsd:anyURI'),
       'sv:runbook':typed('https://docs.example.org/iam/runbook','xsd:anyURI'),
       'sv:escalation':'Example IAM on-call team, then federation operations',
       'sv:changeManagement':'Reviewed deployment changes and maintenance notice',
       'sv:backupPolicy':'Synthetic policy: daily backup, quarterly restore test',
       'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:operator','@type':'schema:Organization','schema:name':'Example global service operator'},
      {'@id':'ex:security','@type':'sv:SecurityProfile','sv:protocol':'OIDC',
       'sv:authorizationPolicy':typed('https://docs.example.org/iam/policy','xsd:anyURI'),
       'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:allocation','@type':'sv:ResourceAllocation','sv:resource':ref('ex:compute'),
       'sv:allocationKind':'request','sv:metric':'memory-bytes','sv:quantity':ref('ex:memory'),
       'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:compute','@type':'sv:InfrastructureResource','sv:resourceKind':'compute'},
      {'@id':'ex:memory','@type':'qudt:QuantityValue','qudt:numericValue':typed('4294967296.0','xsd:decimal'),
       'qudt:unit':ref('unit:BYTE')},
      {'@id':'ex:objective','@type':'sv:ServiceObjective','sv:metric':'availability',
       'sv:comparator':'>=','sv:window':typed('P30D','xsd:duration'),
       'sv:quantity':ref('ex:availability-target'),'sv:evidence':ref('ex:evidence')},
      {'@id':'ex:availability-target','@type':'qudt:QuantityValue','qudt:numericValue':typed('99.9','xsd:decimal'),
       'qudt:unit':ref('unit:PERCENT')},
    ]
    g=Graph().parse(data=json.dumps({'@context':c,'@graph':records}),format='json-ld')
    write_graph(g,'examples/global-service-template')

def registration_examples():
    from sitecaps_adapter import import_service
    for scope,semantic,dep in [
        ('local','synthetic-performance','https://example.org/srcnet/espSRC/synthetic/deployment'),
        ('global','global-service-template','https://example.org/srcnet/global/deployment')]:
        data=json.loads((ROOT/f'examples/sitecaps-{scope}.synthetic.json').read_text())
        g=import_service(data,scope,'https://sitecaps.example.org/api/v1')
        record=next(g.subjects(RDF.type,SV.SiteCapsRecord))
        g.parse(ROOT/f'examples/{semantic}.ttl')
        g.add((URIRef(dep),SV.registration,record))
        write_graph(g,f'examples/sitecaps-{scope}.synthetic')

if __name__=='__main__':
    vocabulary(); examples(); global_template(); registration_examples()
