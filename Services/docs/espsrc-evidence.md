# espSRC instance and provenance

This is a curated example from operator-provided configuration history dated
2026-09-29 to 2026-10-02. It is **not** a live scan, a SiteCaps dump, or proof of
current availability. Generation date: 2026-10-06.

| Item | Included assertion | Evidence / qualification |
|---|---|---|
| Production platform | k3s/Kubernetes on OpenStack, shared CephFS | Reported configuration; no current node count or resource totals asserted |
| CANFAR | `https://canfar.espsrc.iaa.csic.es`, production platform | Reported public endpoint, not probed for health |
| Skaha | App `1.4.0`, Helm chart `1.7.0` | Reported configuration, with separate `SoftwareRelease` entities |
| Release | `espsrccanfar-science-platform` | Reported HelmRelease name |
| Namespaces | `skaha-system`, user workloads `skaha-workload` | Reported configuration |
| Cavern / PosixMapper | Components in `skaha-system` | Reported deployment; no SiteCaps type invented for PosixMapper |
| SODA | Local service in `espsrcsoda` | Sync/async registration endpoints not known; no type assumed |
| PrepareData | Local staging service in `preparedata` | Reported deployment; Flux suspension does not imply service disablement |
| Gatekeeper | Local authorization component | Reported deployment; namespace and endpoint omitted |
| Data lake | Local storage associated with CephFS | Rucio server global type not used for local RSE storage |
| Notebook | Capability realized by Skaha | Does not assert a separate JupyterHub at IAA |
| IAM | `https://ska-iam.stfc.ac.uk/`, global service consumed by espSRC | Reported identity-provider configuration; hosting and version omitted |
| Science Gateway / distribution / registry | Existing global catalogue identities | Architectural placeholders, marked proposed; no deployment claim |
| Dependencies | CANFAR→Skaha, Skaha→IAM/Cavern, Cavern→PosixMapper, SODA/PrepareData→data lake | Architectural interpretation marked proposed, not observed runtime traces |

Private IP addresses, secret paths, credentials, user mappings and personal
contact data are omitted. Stable new example IRIs use `example.org`; original
catalogue and logical service identities retain their original `w3id.org` IRIs.

All local deployment health values are `unknown`. Earlier PVC and metrics
incidents are not used to assert today's state. Application version does not
mean that every pod has been observed running that version.

## Fields required before an actual SiteCaps export

* Actual registration UUID, node/site names, parent site/compute identifiers.
* Exact accepted type and scope of each registered endpoint.
* Required service fields: name, version, prefix, host, port, path, attributes,
  downtime and administrative flag; `is_mandatory` for local service objects.
* Associated compute/storage-area UUIDs when present.
* Current read evidence and an approved mapping to the logical service/deployment.

These are intentionally not inferred from the espSRC display name, an IVOA ID
or a Kubernetes namespace. `SPSRC` appears in API examples, but its relationship
to a specific live espSRC registration is not verified here.

For performance and resource modelling, use `synthetic-performance.*` as a
structural example. Its 0.25 s latency, 99.5% objective and 8 GiB request are
explicitly fictitious; the global template's 99.9% objective is also fictitious.
They must never be presented as espSRC benchmark results or agreed SLAs.
