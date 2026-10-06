# SRCNet service semantic model — SiteCaps profile 0.1.0

An additive, proposed extension to the existing SRCNet model. It describes local
and global services at operational, functional, performance, administration and
infrastructure levels, with an **offline adapter tested against the deployed
SiteCaps 0.3.98 OpenAPI contract** retrieved on 2026-10-06.

This is not an officially adopted SRCNet ontology or a live inventory. The
`https://w3id.org/srcnet/services#` namespace is a proposal and is not registered
by this change. No production API changes are made by this package.

## Start here

* [Diseño y guía en español](docs/design-es.md): architecture, dimensions and interpretation.
* [Migration from the original model](docs/migration.md): exact identities and mappings.
* [SiteCaps contract and field mapping](docs/sitecaps.md): compatibility boundaries and operations.
* [Vocabulary reference](docs/vocabulary.md): every class and property.
* [Evidence and espSRC example](docs/espsrc-evidence.md): known facts and deliberate omissions.
* [Validation](docs/validation.md): reproducible checks and limitations.

## Files

| Path | Purpose |
|---|---|
| `ontology/services.ttl`, `ontology/services.jsonld` | Equivalent OWL/RDFS vocabulary serializations |
| `ontology/context.jsonld` | Self-contained JSON-LD prefixes; no remote context resolution |
| `ontology/shapes.ttl` | SHACL data-quality rules |
| `examples/espsrc-services.{jsonld,ttl}` | Dated operator-reported espSRC example; original service identities |
| `examples/synthetic-performance.{jsonld,ttl}` | Explicitly synthetic metrics, target and allocation |
| `examples/global-service-template.{jsonld,ttl}` | Synthetic global deployment using the same five dimensions |
| `examples/sitecaps-*.synthetic.*` | Native SiteCaps local/global objects and semantic projections |
| `sitecaps/vendor/` | Retrieved contract, schema/type snapshots, provenance and upstream licence |
| `tools/sitecaps_adapter.py` | Offline import/export and safe nested replacement function |
| `tools/build_model.py` | Rebuild vocabulary and espSRC/performance examples |
| `queries/` | SPARQL competency questions bridging old and new data |
| `tests/` | Contract, round-trip, graph-equivalence, SHACL and preservation checks |

## Run locally

From the repository root, using Python 3.11 or newer:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r Services/requirements.txt
python -m pytest -q Services/tests
```

Convert the **synthetic** local-service fixture into a graph and back:

```bash
python Services/tools/sitecaps_adapter.py import \
  Services/examples/sitecaps-local.synthetic.json /tmp/service.jsonld \
  --scope local --registry https://sitecaps.example.org/api/v1
python Services/tools/sitecaps_adapter.py export /tmp/service.jsonld /tmp/service.json
```

The registry argument namespaces identity. Use the actual registry base when
importing a real response, so identical UUIDs in different installations cannot
merge accidentally. No request is sent to that URL.

Use `.ttl` for Turtle output. `export` accepts JSON-LD or Turtle and requires
exactly one `sv:SiteCapsRecord`. It validates required fields, types and UUIDs,
preserves unknown JSON fields, and rejects conflicting maintenance edits.

To load espSRC into a triple store, load `ontology/services.ttl` plus
`examples/espsrc-services.ttl`, then run `queries/local-services.rq`. It can be
joined with the original graph because the catalogue and service IRIs are kept.
Do not load the old empty template as production assertions: blank strings are
placeholders, not measurements or valid identifiers.

## Compatibility statement

Compatibility means validated local/global **service-object** import/export,
not that the API understands OWL, accepts arbitrary new service types, or accepts
the full extended graph as a request body. Details beyond its native contract
live in an external graph; `other_attributes.srcnet_semantic` can reference it.
That key is an extension convention proposed here, not an existing SiteCaps
standard. The adapter does not register, enable, disable or delete anything.

The live `/services/types` snapshot agrees with the pinned OpenAPI. The source
repository's later `main` includes `job_gateway`, absent from the deployed
snapshot: do not silently use source-main types against the deployed API.

The semantic graph can represent Science Gateway, PosixMapper and a data lake
even when they have no corresponding service type in this SiteCaps version.
An unsupported type is not silently converted to `iam`, `jupyterhub` or `rucio`.
