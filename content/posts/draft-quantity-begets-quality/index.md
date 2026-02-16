---
title: "DRAFT: Quantity begets Quality?"
draft: true
categories: ["Medium Archive"]
---

---

### DRAFT: Quantity begets Quality?

![Photo by Simon Maage on Unsplash](https://cdn-images-1.medium.com/max/800/0*Hcp86elPVjWnqjdL)
*Photo by Simon Maage on Unsplash*

A favorite saying of the military and oft-attributed to Stalin.

> Quantity has a quality all its own

For the machine translation projects by Google, this is what makes their machine translation models so powerful. They have immense amounts of parallel texts (English/French, German/Italian, etc translations). This allows them to throw enough data at the problem of building machine translation models without having to inject prior knowledge of the languages into language translation model building. Prior efforts had all tried to add prior knowledge into the language-translation models due to limited training data.

Prior knowledge in machine translation you can inject syntax knowledge of the language into the translation models or even the semantics of particular terms. For biology, you can add knowledge of what proteins interact, and their contextual environments (e.g. disease state, cell type, etc) to filter relevant results from noise in the data.

When there are too many degrees of freedom for the problem you are working on in biology (which appears to be most of them in molecular biology) — you need a lot of data to provide enough statistical power to get an answer. This is why clinical trials often have to have hundreds to hundreds of thousands of participants to ‘power’ the trial effectively. There are many clinical trials that would be wonderful to do that we just don’t have enough patients (not enough people in the world — not even if you were able to include every person ever born). For example, what is the ideal diet matched with the ideal gut microbiome? I’m not sure there would be enough statistical power if there were as many people as atoms in the solar system or even galaxy to answer that question. The more tightly you constrain the question and the more degrees of freedom ***you can remove***, the less data you need to drive to a statistically significant answer.

[In complex biology, prior knowledge is power](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3102020/) [Ideker, et al 2011], BioDati Studio is all about capturing biological knowledge in a computable format to power knowledge-driven algorithms and power data science. When you have genomic data for a set of patients with a disease that results in a large number of mutations or variants, using prior knowledge can bridge the gap between statistically underpowered data and the phenotype of interest by reducing the degrees of freedom — focusing the attention on relevant biology.

Further, statistical significance should always be evaluated in terms of biological significance. Using prior knowledge made eminently accessible by Biodati Studio using an open-standard language for Biology, you can more easily interpret statistical results in terms of biology.
