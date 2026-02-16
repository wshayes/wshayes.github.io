---
title: "BEL 2.1 Enhancements"
date: 2018-12-10T20:31:09.343Z
categories: ["Medium Archive"]
---

---

![Photo by David Clode on Unsplash](image.jpg)
*Photo by David Clode on Unsplash*

The BEL Language committee has approved four BEL Enhancement Proposals (BEP) that are being released as BEL version 2.1.0.

The changes are listed below in their BEPs below:

- [BEP-0001 — population abundance function](https://github.com/belbio/bep/blob/master/docs/published/BEP-0001.md)
- [BEP-0003 — noCorrelation relationship](https://github.com/belbio/bep/blob/master/docs/published/BEP-0003.md)
- [BEP-0004 — equivalence relationship](https://github.com/belbio/bep/blob/master/docs/published/BEP-0004.md)
- [BEP-0005 — namespaces validated via regex](https://github.com/belbio/bep/blob/master/docs/published/BEP-0005.md)

These changes are more formally specified in the BEL Specification 2.1.0 in a computable format (custom [YAML](https://github.com/belbio/bel_specifications/blob/master/specifications/bel_v2_1_0.yaml) or [EBNF](https://github.com/belbio/bel_specifications/blob/master/specifications/bel_v2_1_0.ebnf)).

#### [BEP-0001 — population abundance function](https://github.com/belbio/bep/blob/master/docs/published/BEP-0001.md)

The biggest change is the populationAbundance, pop(), function that allows us to capture microbiome changes, cell population changes, even ecosystem changes (e.g. increased wolf population decreases deer population). We are looking forward to the additional novel use cases you develop for the pop() function. Please share with us additional ways you figure out how to use pop().

Examples:

```
# Penicillin decreases the population of Streptococcus entericusa(CHEBI:penicillin) decreases pop(TAX:1123302)# California Mule Deer increases population of gray wolvespop(TAX:598490) increases pop(TAX:9612)# Firmicutes bacteria increases obesitypop(TAX:1239) increases path(MESH:Obesity)# A heterogeneous population of microbiome bacteriacomposite(pop(TAX:xxxx), pop(TAX:yyyy)) increases ...# A drug decreases the population of adipocytesa(CHEBI:metformin) decreases pop(MESH:"Adipocytes, White")# P. falciparum invasion of RBCs increases malariacomplex(pop(NCBI:txid5833), pop(CL:erythrocyte)) increases path(DO:malaria)#S. typhimurium in complex with L-ficolin (an opsonin) enhances phagocytosis [PMID:8576206]complex(pop(NCBI:txid90371), p(HGNC:FCN2)) increases bp(GO:phagocytosis)
```

#### [BEP-0003 — noCorrelation relationship](https://github.com/belbio/bep/blob/master/docs/published/BEP-0003.md)

We also added the ability to talk about negative results using the noCorrelation relationship to document that no correlation positive or negative was found. The BEL causesNoChange relationship is similar in concept, but requires the assessment of a causal relationship.

Examples:

```
# In systemic lupus erythematosus patients, TNFSF13B was significantly correlated with disease activity, but no significant correlation was found between IL10 and disease activity.path(DO:“systemic lupus erythematous”) noCorrelation p(HGNC:IL10)# In patients with rheumatoid arthritis, plasma leptin concentrations did not correlate with BMI. bp(MESH:“Body Mass Index”) noCorrelation a(CHEBI:Leptin)
```

#### [BEP-0004 — equivalence relationship](https://github.com/belbio/bep/blob/master/docs/published/BEP-0004.md)

A lot of equivalencing is managed through terminologies (e.g. HGNC:AKT1 is synonymous to EG:207), but BEL Functions are not possible to equivalence using terminologies along except for one special case that is not recommended.

Examples of the equivalence relationship:

```
a(CHEBI:”amyloid-beta polypeptide 40") eq p(HGNC:APP, frag(672_711))
```

```
g(HGNC:MDGA2, var(c.*1638C>A)) equivalentTo g(dbSNP:rs1235)
```

```
complex(FPLX:”Adaptor_protein_III”) eq complex(p(HGNC:AP3B1), p(HGNC:AP3D1), p(HGNC:AP3S1), p(HGNC:AP3S2))
```

It is not recommended to use the equivalence relationship like so:

```
g(HGNC:AKT1) eq g(ENTREZ:207)
```

#### [BEP-0005 — namespaces validated via regex](https://github.com/belbio/bep/blob/master/docs/published/BEP-0005.md)

For developers of BEL-based platforms, the regex validation of namespaces will help in syntax validation of BEL Assertions.

Example:

```
Patterns for namespaces are listed on https://identifiers.org. For example, the PFAM page contains the regular expression for its standardized identifiers (^PF\d{5}$)
```

```
NAMESPACE PFAM should have PATTERN "^PF\d{5}$"
```

### Credits

John Bachman, Natalie Catlett, William Hayes, and Charlie Hoyt served on the BEP committee to approve these changes.

### Additional Notes

Anyone can propose BEP’s by following the [instructions](https://github.com/belbio/bep). If you have a change to BEL that you would like to propose and are having trouble developing the BEP, you can contact me or anyone else on the committee for assistance.
