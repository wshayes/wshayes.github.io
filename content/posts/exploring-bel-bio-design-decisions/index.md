---
title: "Exploring BEL.bio Design Decisions"
date: 2018-02-01T14:01:07.128Z
categories: ["Medium Archive"]
---

---

![Photo courtesy of: Bich Nguyen Vo](10KderNXFsE1UavzXkLllJQ.jpeg)
*Photo courtesy of: Bich Nguyen Vo*

We revamped some of the conventions and approaches developed and shared in the OpenBEL Platform. I’m visiting some of those design decisions here. OpenBEL provided ideas and approaches many of which have been deployed in [BEL.bio](http://bel.bio), some of which yielded learnings that drove changes. Without OpenBEL paving the way, we would not be where we are now.

> [Background](https://medium.com/@williamhayes/my-love-affair-with-json-edaca39e8320) on JSON/YAML driving some of the BEL.bio design decisions.

### BEL Specification

One of the biggest enablers of the BEL.bio redesign is the BEL Language Specification YAML file for each BEL version. This file captures the syntax and semantics of the BEL Language and drives our ability to provide syntax and semantic support and validation. An example of the proteinAbundance function signature (part of it):

```
proteinAbundance:      func_type: primary      name: proteinAbundance      signatures:      - arguments:        - type: NSArg          position: 1          values:          - Protein        - optional: true          type: Modifier          values:          - location          - fragment        - multiple: true          optional: true          type: Modifier          values:          - variant          - proteinModification
```

All of the BEL functions, function arguments, and relations are defined in this file. We only have the one file for BEL 2.0.0 at this point, but it completely drives all BEL parsing, BEL completion and syntax/semantic validation. The BEL.bio API has been setup to work off of as many different versions of BEL as you would like as long as there is a BEL Specification for that version in the python bel package. We will provide a configuration option in the future to allow you to create your own BEL Specifications for testing out new BEL features before submitting them for inclusion into the next version of BEL.

> A side effect of this is that we are rigorously using semantic versioning now for the BEL language.

### BEL Namespaces

First off, what is a BEL Namespace? It’s simply a terminology that is designed to be unambiguous regarding the semantics of the entity or concept being described. An example is ‘AKT1’, this is possibly the name of a gene, mRNA or protein in an organism — which organism, what type of entity is it? The BEL Namespace form would prefix it with a label: HGNC:AKT1. Now we know that it is a Human Gene Nomenclature Committee gene symbol and also know that it can be a gene, mRNA or protein (we can’t determine what type of entity until it is used in a BEL function such as `geneAbundance(HGNC:AKT1)`or `proteinAbundance(HGNC:AKT1)` ).

One change we made from OpenBEL was to provide one prefix per Namespace and make the Namespaces smarter. This greatly simplifies the number of Namespace prefixes for which a user has to keep track. OpenBEL used GOBP, GOBPID, GOCC, GOCCID, etc for different subsets of the [Gene Ontology](http://www.geneontology.org/). The different prefixes would identify GO Biological Process terms by name or id (e.g. GOBP vs GOBPID). BEL.bio now just uses ‘GO’ for all of these.

This required creating an intermediate data form for capturing BEL Namespace information about individual terms in a Namespace that could capture BEL entity types, annotation types, species if relevant, alternate IDs, and obsolete IDs. For full details on what is captured for a term in a Namespace, [here is the full JSONschema in YAML format](https://github.com/belbio/schemas/blob/master/schemas/terminology-0.1.0.yaml).

The BEL Namespace functionality exposed through the [BEL.bio API](http://apidocs.bel.bio/) allows for searching for terms that meet specific requirements for entity types, annotation types or species. Each GO term is tagged with the specific entity types and annotation types associated with that term. Every [EntrezGene](https://www.ncbi.nlm.nih.gov/gene) (EG) Namespace ID has the species type associated with it.

Every BEL function specified in the BEL Specification YAML file has the entity types allowed for any Namespace arguments defined in the function specification. Providing completion support for BEL Assertions or semantic validation is dependent on the specific term record entity types associated with the term not the BEL Namespace prefix.

#### Equivalencing and Orthologization

OpenBEL required re-building all of the terminologies together since a single UUID (universal ID) was created for each equivalence set and orthology set. This meant that making a small change to one term required rebuilding the entire dataset of namespaces and orthology data before deploying that change. We are now using the [ArangoDB](https://www.arangodb.com/) graph database for capturing equivalences and orthologies. This allows us to load up individual terms or single Namespaces at a time and still be able to equivalence them with other terms (as long as equivalences are captured during the terminology collection process).

### BEL Annotations

BEL Annotations were less rigorously defined in OpenBEL. We have shifted to using BEL Namespaces and capture BEL Annotations with an Annotation type, an Annotation ID using the full Namespace argument, e.g. DO:arthritis and an Annotation label for easier human review. The OpenBEL Annotation basically consisted of the Annotation type and the Annotation label.

Using a BEL Namespace for the Annotation ID, provides unambiguous annotations for BEL Nanopubs. It will also allow us (in the future) to be able to query hierarchically for lung-related BEL Assertions by processing the hierarchical structure of Uberon or an equivalent anatomical namespace so that we can find any lung, lung substructure or lung tissue related BEL Assertion.

### BEL Resource Generation

There are now three different philosophies found in BEL resource generation.

- [OpenBEL created a pipeline](https://github.com/OpenBEL/resource-generator) using shared python libraries and overridden Python Classes to generate OpenBEL Namespace belanno and beleq files as well as Semantic Web-based [SKOS](https://www.w3.org/2004/02/skos/) files for use in triplestores
- [Bel2bio](https://github.com/bio2bel) uses a separate github repo all under the bel2bio Github organization for creating each OpenBEL Namespace belanno and beleq BEL corpus generator with mostly independent code except for pybel
- [BEL.bio Resource Generation](https://github.com/belbio/bel_resources) uses a single github repo for collecting and processing BEL Namespaces and other resources and some shared code between mostly independent scripts to collect/reformat source databases into BEL Namespaces

The OpenBEL resources pipeline just became too much overhead for anyone to quickly dive into and required a fair amount of dedication to working with it. Bel2bio and BEL.bio approaches make it much easier to jump in and create a new BEL Namespace or debug one. Separate github repositories make it easier to develop and maintain these without impacting other Namespace generators. A single github repository makes it easier to administer and maintain a set of BEL resource generators.

We have focused on implementing the BEL.bio resource generators to be efficient in downloading and processing source data into terminologies/orthologies and other BEL resources.

- We attempt to check if the source database (e.g. Swissprot or EntrezGene) are newer than what has been downloaded.
- If newer or cannot tell and X days have passed, we re-download the source data used to generate the Namespaces to a single download directory and compress anything that is not already compressed.
- We then process the downloaded data into the [terminology JSONschema](https://github.com/belbio/schemas/blob/master/schemas/terminology-0.1.0.yaml) format using gzipped JSONLines for storing on disk.
- We can then load all or any of the individual terminology datasets into the BEL.bio API server using a load script.

We still have a lot to do to make this process simpler to administer and maintain. It is not easy or simple to source and convert all of the different databases available into BEL resources. We think this strikes a reasonable balance between simplicity and complexity.

### OpenBEL Data formats

We are not supporting the [BELScript data format](http://openbel.org/language/version_1.0/bel_specification_version_1.0.html#bel-script) beyond converting it into the [BEL Nanopub JSON](https://github.com/belbio/schemas/blob/master/schemas/nanopub_bel-1.0.0.yaml) format. BELScript is a custom format which requires a custom parser. It is not well supported given that OpenBEL code is not supported at this point. JSON is strongly supported by almost all programming languages.

Even if you don’t validate using the BEL Nanopub JSONSchema, you can still easily work with the BEL Nanopub JSON format. Parsing and loading it is as simple as loading a JSON file compared to the custom code you need to parse a BELScript file.

We are also not supporting the belanno and beleq files used for OpenBEL Namespaces. They are again custom data formats which require custom parsers. They do not capture enough information to serve the needs of the smarter Namespace data format required.
