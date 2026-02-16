---
title: "A Typical BioDati Workflow"
draft: true
categories: ["Medium Archive"]
---

---

### A Typical BioDati Workflow

![](https://cdn-images-1.medium.com/max/800/1*84FPpj-eeEWfrePnUvTckA.png)

It would be helpful to read [What is BEL?](https://medium.com/biodati/what-is-bel-8df1a549760f) first.

A simple truth: Biologists communicate in networks. Everything in biology ultimately comes down to a molecule(s) interacting with another molecule(s). These interactions are naturally captured in network diagrams or graph databases.

Unfortunately, the tools that biologists have (journal articles, powerpoint, etc) don’t lend themselves well to this paradigm. [BioDati Studio](http://biodati.com) is designed to make working with network biology straightforward and easy (okay, easier :)

***Insert image of BEL Nanopub -> EdgeStore -> Network -> NetworkStore here***

A full-cycle flow of knowledge through BioDati is:

- Capture biological knowledge in a BEL Nanopub
- Convert BEL Nanopub into BEL Edges
- Load BEL Edges into EdgeStore
- Extract relevant Edges into a Network
- Save the Network into the NetworkStore
- Share the Network for collaboration

This full-cycle workflow doesn’t represent what will typically happen. People do not always follow the golden path. Most biologists will start with an interest in a particular biological context (e.g. human, lung cancer, stage 1, lung tissue) and:

- Extract relevant Edges from the EdgeStore to build a network representing current knowledge regarding human lung cancer disease context and the changes in lung epithelial cells
- As they progress in their research or uncover new biology in the literature, they will add new BEL Nanopubs
- These Nanopubs get automatically added as Edges into the EdgeStore
- These new Edges can then be added to the Network. The really great part is they will be able to show all the full supporting evidence for that Edge in the Network

This may seem a convoluted way to build a network because someone can just build a network of nodes and edges in Powerpoint directly without this effort to create a BEL Nanopub. However, the BEL Nanopub captures your new findings with its supporting evidence, experimental context and metadata. It is formatted in a standard way that can be validated and used in data analytics. This knowledge is also easily shared with the rest of the members of the company, also know as sharing knowledge capital.

One of the major advantages is you now have Networks where you can investigate the assumptions behind each and every Edge. An Edge may be supported directly by one or more BEL Nanopubs, but you can also query the EdgeStore to see what other BEL Nanopubs match the same edge (which might have similar or completely different context). You also have on tap a database of possible biology (the EdgeStore) that you can use to insert more knowledge (Edges) into your Network.

![Creating a Nanopub in the editor](https://cdn-images-1.medium.com/max/800/1*GBrYmMniI6fGywRP9kediA.png)
*Creating a Nanopub in the editor*

***Insert image of a BioDati Studio network with Nanopub supports here***
