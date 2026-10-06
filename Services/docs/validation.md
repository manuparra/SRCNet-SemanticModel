# Validation and reproducibility

Run `python -m pytest -q Services/tests` from the repository root after installing
`Services/requirements.txt`. Tests do not need network access or credentials.

Validation performed on 2026-10-06: **66 tests passed** under Python 3.12.
RDFLib emits dependency deprecation warnings; these are not validation failures.
`git diff --check` also passed. All checks are local and reproducible.

The suite checks:

* Turtle and JSON-LD graph equivalence for the ontology and instance examples.
* SHACL conformance of examples; a missing quantity unit fails validation.
* Native JSON → RDF → native JSON equality for both local and global services.
* Every accepted type in the retrieved SiteCaps enumeration.
* Preservation of unknown JSON, nested attributes, optional-field absence,
  parent context, separate associated/parent compute IDs and downtime records.
* Rejection of invalid UUIDs, malformed flags/ports, unknown types, inconsistent
  scopes, null required strings and invalid downtime intervals.
* RDF scalar editing, duplicate-property rejection and maintenance projection conflicts.
* Isolation of registration identities across API installations.
* Non-mutating node replacement, sibling preservation and parent mismatch rejection.
* Old service identities, absence of invented espSRC UUIDs and vocabulary coverage.

The SHACL profile validates the semantic layer. The adapter's pinned OpenAPI
validation additionally enforces API-specific enums and required native fields.
SHACL alone does not prove SiteCaps-exportability. JSON Schema alone does not
prove service health, complete inventory, SLA compliance or correct ownership.

Regenerate vocabulary and semantic examples:

```bash
python Services/tools/build_model.py
```

The standalone context is copied into each JSON-LD serialization, so parsing
does not require a resolvable `w3id.org` namespace or fetching a remote context.
Byte order may differ between RDFLib serializations; RDF graph equality is the
reproducibility criterion.

For a new API version: capture its type and schema endpoints plus OpenAPI,
record provenance, compare required fields and enums, update the adapter profile,
and run fixtures against that version. Do not simply change `contractVersion`.

No production SiteCaps writes or authenticated end-to-end tests were performed.
No GitHub Actions workflow is introduced automatically; this test command can
be added to the repository's chosen CI after review.
