---
title: "Computable Knowledge has Superpowers!"
date: 2021-02-24T18:53:12.811Z
categories: ["Medium Archive"]
---

---

![Photo by Chris Lawton on Unsplash](https://cdn-images-1.medium.com/max/800/0*4-0T2IrF262klENM)
*Photo by Chris Lawton on Unsplash*

One of the side effects of capturing biological knowledge in a computable language is the ability to transform it into new forms. One of the questions we’ve been asked before about [BEL](https://bel.bio) (Biological Expression Language) is whether there are multiple ways to capture the same knowledge. Basically, does BEL force people to capture the same biological relationships in exactly the same way? The short answer is NO.

BEL provides a lot of flexibility. Biology requires that flexibility given how weird, wonderful, and wild biology can be. We are always finding edge cases that prove nothing is without exception in biology. Given the similarities in BEL to programming languages, it’s absolutely expected that you could find multiple ways to capture the same biology in BEL in different ways.

One example is a reaction:

```
rxn(reactants(p(A, loc(intracellular)), products(p(A, loc(extracellular)))
```

can also be presented as translocation:

```
tloc(p(A), fromLoc(intracellular), toLoc(extracellular))
```

or a secretion event:

```
sec(p(A))
```

> **This is one of the superpowers of using a computable language for biology.**

We have had normalization (or canonicalization) to support normalizing namespaces in BEL (e.g. EntrezGene:207 converted to/from *HGNC:AKT1*). This allows users to use the name or ID that they are comfortable with. We have now added semantic normalization to convert multiple versions of the same biological assertion into a standardized format.

So now whenever we see a secretion event represented as a ***rxn()***, we can convert it automatically to sec(). Or if the ***rxn()*** is not a ***sec()*** but another type of translocation, we can convert it to a ***tloc()*** as a more optimal or preferred format for BEL.

While parsing BEL Assertion during the curation process, we can also suggest preferred formats for capturing biological knowledge, helping to guide and teach new curators.

**This is one of the superpowers of using a computable language for biology.** The ability to normalize biology automatically so it’s easier to use by end-users as well as data analysts. More consistent knowledge that adheres to best practice is easier to use in prior-knowledge driven algorithms and makes it more reusable!
