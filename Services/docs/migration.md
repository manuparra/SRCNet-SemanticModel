# Connecting the original graph and the services extension

Baseline: original repository commit `c82254411b70cb1826fac2b85bbea7f56f3439a1`.
The original `Model/` files and their queries are not rewritten. Load the new
graph beside the old graph; their shared IRIs provide the join.

## Entity mapping

| Original representation | Extension | Migration rule |
|---|---|---|
| `src:SRC` at `/node/espsrc` | Same entity | Keep identity and organisational role |
| `dcterms:hasPart` → `src:Node` at `/node/espsrc-node` | Same entity, explicit `sv:Site` linked by `sv:partOfNode` | SiteCaps Node/Site must be mapped explicitly; display names are not API IDs |
| `src:localServiceCatalog` and `src:globalServiceCatalog` | Same predicates and catalogue IRIs | Preserve existing catalogue queries |
| `dcat:service` → `dcat:DataService` | Same service, additionally `sv:Service` | Add a type, do not rename the service |
| `src:serviceId` | `sv:siteCapsId` on a separate `SiteCapsRecord`, if verified | Do not assume any old string is a SiteCaps UUID |
| `src:serviceVersion` | `SoftwareRelease` associated with the relevant deployment | Identify the component first; chart version is not app version |
| `dcat:endpointURL` | `Endpoint` with role, evidence and URL IRI | Retain old endpoint triples if needed; avoid automatic equivalence across protocols |
| `src:resourceRequirements` | `ResourceAllocation` with `allocationKind="request"` | Keep original requirements; never convert them into installed capacity |
| `src:hasJupyterNotebook` | Notebook functional capability | Does not establish a JupyterHub deployment |
| `src:hasAlert` | Operational profile and monitoring/health endpoint references | Detailed alert-rule vocabularies can be added without redefining old alerts |
| Empty strings in original template | Omitted assertions or explicit unknown operational state | Do not generate fake zeros, false flags or empty numeric values |

We intentionally do **not** assert `owl:sameAs` between SiteCaps parent nodes,
registered services, logical services and deployments. They represent different
things. `sv:Service rdfs:subClassOf dcat:DataService` follows the repository's
existing catalogue convention. This broad convention also covers IAM; a future
general Service super-class may be considered without changing old identities.

## Original service identities

All entries below retain the prefix `https://w3id.org/srcnet/service/`.

| Original suffix | New interpretation | SiteCaps mapping decision |
|---|---|---|
| `espsrcscienceplatform` | Logical CANFAR platform | Candidate local `canfar`; needs actual registration |
| `espsrc-notebook` | Notebook capability realized by Skaha | Do not automatically map to `jupyterhub` |
| `espsrcsoda` | Logical SODA service | Register separate `soda_sync` / `soda_async` endpoints only when confirmed |
| `espsrc-datalake` | Logical local data lake | Storage / StorageArea (`rse`) is distinct from global `rucio` service |
| `espsrc-visualization` | Existing visualization catalogue entry | Preserved in original graph; do not invent a deployed CARTA service |
| `espsrcmonitoring` | Existing monitoring catalogue entry | Preserved in original graph; no current endpoint assumed |
| `authentication` | Global IAM | Global `iam` only after verifying the specific registration |
| `sciencegateway` | Global Science Gateway | Not an accepted type in pinned API; semantic-only |
| `datadistributionplatform` | Logical federated data distribution | May comprise multiple services; no automatic equality to Rucio |
| `registryservice` | Logical registry | Semantic-only in this contract |

New components include `espsrc-skaha`, `espsrc-cavern`, `espsrc-posixmapper`,
`espsrc-preparedata` and `espsrc-gatekeeper`. These are proposed semantic IRIs,
not SiteCaps IDs or IVOA registry IDs. A stable logical identity survives a
namespace move; deployments and their dated evidence record configuration.

## Incremental adoption

1. Load the extension ontology and a clean instance graph without altering the original ontology.
2. Reuse the original service URI and add `sv:Service`, scope and functional details.
3. Add deployment, hosting site and profiles with evidence. Leave unknown properties absent.
4. Obtain the actual SiteCaps node/site names and service UUID from an authorised read.
5. Import the object with the offline adapter, then link the deployment using `sv:registration`.
6. Validate SHACL and the pinned SiteCaps contract. Inspect unsupported service types.
7. Store detailed RDF externally, optionally linking its stable URI through `other_attributes.srcnet_semantic`.

The espSRC example is at step 3: it is deliberately not a pretend SiteCaps
dump. `queries/legacy-catalog.rq` demonstrates the original-to-new join.
