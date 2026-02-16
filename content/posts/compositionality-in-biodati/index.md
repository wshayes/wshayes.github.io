---
title: "Compositionality in BioDati"
draft: true
categories: ["Medium Archive"]
---

---

### Compositionality in BioDati

![Photo by John Matychuk on Unsplash](https://cdn-images-1.medium.com/max/800/0*BhdFOZBVUN8CVlIR)
*Photo by John Matychuk on Unsplash*

DRAFT — not ready — will probably wait for Lists AND Styles to be deployed first

The word **composition** comes from the Latin *componere*, meaning “put together”. In **computer science**, object **composition** is a way to combine objects or data types into more complex ones.

When I’m speaking about it here, I’m talking about how we manage components of BioDati data and supporting elements. To get right to it, we use the principle of composition to add data or styles to networks. You can also think of nanopubs as components that get merged together into a composition of knowledge that addresses a particular need (e.g. an instance of realized biology based on a specific biological context from the set of possible or potential biology represented by all nanopubs and foundational knowledge).

For our networks, we use the JSON Graph Format (JGF) which focuses on the connectivity of the network and allows adding graph, node, and edge metadata. It purposefully doesn’t include network layout and styling. We use the JSON Style Format (JSF) specification for that. Given a network, we can now use multiple JSF files to easily switch between network styles or use multiple JSF files at the same time that affect different aspects of the network (one JSF may style the nodes and another the edges). These JSF files can also be applied to multiple networks. Many of the network serialization formats we’ve reviewed merge the layout, styles, and connectivity into one file. This is convenient when you need to archive a particular view, but it makes it difficult to personalize the network view for your specific needs.

Much of the use of the biological networks we manage are initially for use visually, but we see extensive value in using these networks for data analytics. For data analytics only the connectivity and semantics recorded in the node and edge metadata really matter. Our compositional approach provides a lot of flexibility as well as making it simpler for computational biologists to use the networks without having to extract the connectivity from a format that is focused first on presentation and layout.

Another major aspect of compositionality is how we manage our Gene Sets or Lists of Nodes/Edges. You can read more about our Lists here XXX. Lists give us the ability to layer different data sets onto networks. Again, we don’t want to embed a specific List into a network. Instead, we can associate one or more Lists to one or more Networks.
