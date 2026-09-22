# SRCNet-SemanticModel

## Description
This repository contains an early but functional semantic prototype of the SKA Regional Centre Network (SRCNet), including an OWL ontology, JSON-LD representations, example instances and SPARQL queries intended to support ongoing development and evaluation of a common semantic model for SRCNet resources and services. The repository is structured around three main directories, each serving a distinct purpose within the semantic framework:

**Model**

The following files are provided to support the execution and validation of the semantic model:

+ Full_context.json
+ SRCNet_model_TestData.json
+ SRCNet_model_TestData.ttl
+ SRCnode_model.json
+ SRCnode_model.ttl
+ conversor_json_rdf.py
+ src_ontology.owl

**Competency_Questions**

Contains SPARQL queries and the corresponding outputs generated from the example SRCNet knowledge graph.

**Diagrams**

Provides graphical representations of the semantic model and its constituent components.

This structure helps demonstrate the consistency and robustness of the proposed SRCNet semantic model, while improving transparency, facilitating reproducibility, and providing a clearer understanding of its architecture and underlying components.

**Future Work**

The following activities are required to consolidate the model into a fully operational SRCNet knowledge representation framework:
  
+ Validation with the wider SRCNet community and domain experts.
+ Definition of competency questions and systematic evaluation against user requirements.
+ Ontology quality assessment and consistency checking.
+ Extension of the model to cover additional SRCNet operational scenarios and services.
+ Development of SHACL validation rules and formal data quality constraints.
+ Testing with real SRCNet deployments and production metadata.
+ Alignment with additional FAIR and astronomy community standards where appropriate.



## Usage

Users can replicate the model template and populate it with their own SRC-related information. The resulting JSON-LD document can then be transformed into RDF, imported into an Apache Jena Fuseki dataset, and queried using SPARQL to support data retrieval, validation, and semantic analysis.


## Contributions

- One: Clone this repository.
- Two: Add your features and suggestions to collaborate on this research project.

## Citation

  Edgar Ribeiro João, Julián Garrido, & Manuel Parra-Royón. (2026). Edgar25-coder/SRCNet-SemanticModel: Source code (Version v1.2.3) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.22897624
  
  Bibtex entry:
  
```bibtex
@software{edgar_ribeiro_joao_2026_22897624,
  author       = {Edgar Ribeiro João and Julián Garrido and Manuel Parra-Royón},
  title        = {Edgar25-coder/SRCNet-SemanticModel: Source code},
  month        = {sep},
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.2.3},
  doi          = {10.5281/zenodo.22897624},
}
```

## License

MIT License
