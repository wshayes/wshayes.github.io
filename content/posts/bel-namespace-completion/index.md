---
title: "BEL Namespace Completion"
date: 2018-02-17T22:59:49.536Z
categories: ["Medium Archive"]
---

---

![Photo by Wyatt Ryan on Unsplash](0IIivr6-g195YK0TV.jpg)
*Photo by Wyatt Ryan on Unsplash*

Term completion is always a challenge — provide the most relevant result with the least amount of user input. The BEL.bio API has two major completion services. One is for BEL Namespaces used in BEL Assertion creation and the other is in BEL Nanopub Annotation creation. Both of these rely upon the BEL.bio API /terms/completions endpoint.

A BEL Namespace is a terminology using the format of PREFIX:value to provide an unambiguous identifier across many different terminologies and databases (EntrezGene, SwissProt, Gene Ontology, MeSH, ChEBI, etc). A namespace may be used in a variety of different ways or represent many different types of concepts. An NLM Medical Subject Heading (prefix MESH) term can be a Disease, Pathology, Gene, Protein, mRNA, CellLine or other concept. Each term object in a BEL Namespace needs to be individually processed with the appropriate metadata added to it.

Given the number of terminologies needed in Biology ([non]species-specific gene/RNA/protein names, disease names, Gene ontology, cell and cell-line names, chemical compound names), there are a lot of terms and concepts to know. It is pretty much impossible for a scientist to know all of the names and terms they need to know especially since the common name in use won’t often match the ‘official’ name.

To support namespace completions, we save each namespace term with a variety of associated information as seen in the [Terminology JSONSchema](https://github.com/belbio/schemas/blob/master/schemas/terminology-0.1.0.yaml) (using HGNC:AKT1 for an example term):

- Namespace prefix (HGNC for Human Gene Nomenclature Committee)
- Namespace value (AKT1)
- Species ID if relevant to the term (TAX:9606 for human)
- ID (HGNC:AKT1)
- Alternate IDs (includes lowercased ID to improve search speed)
- Official name of the term (AKT serine/threonine kinase 1)
- Label (AKT1 — human/UI friendly term to use)
- Entity types (Gene, RNA, Protein — used to filter terms for BEL Assertions)
- Synonyms (RAC, PKB, PRKBA, AKT)
- Obsolete ID’s (none for AKT1)
- Annotation types (none for AKT1 — used to filter terms for BEL Annotations)

This term object is saved to Elasticsearch which handles the completion-based search using this [mapping](https://github.com/belbio/bel/blob/master/bel/db/es_mapping_terms.yml) for Elasticsearch.

#### Example Completion for AKT

> [http://localhost:8181/terms/completions/AKT?size=10&species=TAX:9606&entity\_types=Protein](http://localhost:8181/terms/completions/AKT1?size=10&species=TAX:9606&entity_types=Protein)

Here we are completing on AKT, filtering for human and the Protein entity type.

```
{    "completion_text": "AKT",    "completions": [        {...},        {            "id": "HGNC:AKT1",            "name": "AKT serine/threonine kinase 1",            "label": "AKT1",            "description": "",            "species": {                "id": "TAX:9606",                "label": "human"            },            "entity_types": [                "Gene",                "RNA",                "Protein"            ],            "annotation_types": null,            "highlight": [                "<em>AKT1</em>"            ]        },...
```

#### Finally — tuning the completion search!

Initially, the completion search was fairly simple, we just queried the autocomplete field that we created in Elasticsearch (an Edge NGRAM field) and into which we copied the relevant fields (ID, name, label, synonyms, alt\_ids, etc). After having some real users test it, the feedback was that the results were underwhelming. For example, completing on AKT1 would not float the PREFIX:AKT1 to the top.

Desired features of the term completion:

- Score exact matches to ID the highest (6X)
- Next highest scoring matches would be for exact matches to the namespace value and label (5X)
- Have certain namespaces (where there are overlapping conceptual spaces such as EntrezGene, SwissProt, HGNC) score higher since an HGNC:AKT1 is easier to remember and use than EG:207 (the equivalent EntrezGene namespace value for HGNC:AKT1) — these namespaces are configurable (6X)
- Exact matches to a synonym (3X)
- Autocomplete field match (1X)
- Filtered to only return terms matching the species id if the species id is provided and relevant to the namespace
- Filtered to the entity or annotation types so that we are only looking for namespace values that match the targeted entity or annotation

> The relevant code for the tuned completion search is listed here: <https://github.com/belbio/bel_api/blob/master/api/services/terms.py#L230-L285>

#### Finis

Tuning completions is an iterative affair and can be quite challenging as you can easily make one class of results worse when you make another class of completions results better. This is actually the third iteration. The first iteration used the in-memory Trie-based Elasticsearch completion capability, but we needed the ability to handle more complex filtering than that approach would allow.

If you get a chance to test out our completion endpoint and have some suggestions on making it better, please let us know. Until next time!
