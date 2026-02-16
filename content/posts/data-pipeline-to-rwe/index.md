---
title: "Data Pipeline to RWE"
date: 2021-04-08T13:29:18.861Z
categories: ["Medium Archive"]
---

---

### Data Pipeline to RWE

![Photo by nikko macaspac on Unsplash](https://cdn-images-1.medium.com/max/800/0*_GLwpJyu-XLrR8vW)
*Photo by nikko macaspac on Unsplash*

Real World Evidence (RWE) is built on the backs of many types of aggregated data. Similar but not equivalent data is often aggregated from different providers like hospitals. The similar but not equivalent data results in challenges for interpreting and normalizing these aggregated data into a consistent and usable dataset.

Working with EHR and Claims data sources is first and foremost a data management and normalization challenge and only secondarily a challenge in analyzing the resulting dataset. Only when you have the ingestion of the datasets correctly handled can you start to develop your analytics on top of that data. Further, your analytics often informs how you need to change your data ingestion to normalize your datasets for more effective use leading to iterative processing of your incoming datasets.

The approach that I’ve seen that works best is ELT — Extract-Load-Transform rather than ETL (Extract-Transform-Load). It seems a little odd that switching out the Load/Transform steps would have a significant effect. The reason ELT is preferred is that until you have a solid and mature data transformation process you will likely need to transform the raw datasets over and over again.

Given the need to iterate on your data transformation, you’ll want a data transformation service that you can easily re-run in a timely fashion for follow-up iterations. Timely is difficult to define, but the faster you can iterate your datasets, the faster you can make progress and not depend on your data analytics team having to apply a lot of temporary data fixes. It also alleviates the mental overhead of dealing with ephemeral data bugs and the more likely issue of having persistent data bugs that become entrenched in your analytics codebase because it takes weeks/months to update your normalized databases. I personally prefer the ability to update the normalized database from the raw databases at least in one overnight span and since most of the transformation process is highly parallelizable, this should always be achievable using a reasonably engineered data pipeline.

#### Defining your data transformations

Now that you understand what the overall flow should be (ELT). How do you define the data transformations needed for different data sources? This always requires healthcare data domain expertise and skills in *data archeology*. I’ve rarely found databases described well and never in a computable and standardized format with proper semantics. Sure, the source database schema might be shared as a beautiful diagram, but that doesn’t tell me that the number I see in the column for patient weight is in kilograms vs pounds. Is the creatine measure presented in *μmol/L* or *mmol/L*? Are you using molar or mass units for lab results? There are always legacy data issues carried forward in new EHR systems, and data standards are progressing apace — resulting in even more data legacy issues. The owners of an EHR system usually/mostly understand their data, but typically when transferring it to someone else to aggregate and analyze, the effort is on dumping it out to hand off to the aggregator and not in fully documenting the data.

#### DSL to the rescue!

DSL stands for **Domain Specific Language**. A DSL provides a high-level and computable language for a specific and specialized purpose. Some examples of DSL’s are:

- [MermaidJS](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggVERcbiAgICBBW0NocmlzdG1hc10gLS0-fEdldCBtb25leXwgQihHbyBzaG9wcGluZylcbiAgICBCIC0tPiBDe0xldCBtZSB0aGlua31cbiAgICBDIC0tPnxPbmV8IERbTGFwdG9wXVxuICAgIEMgLS0-fFR3b3wgRVtpUGhvbmVdXG4gICAgQyAtLT58VGhyZWV8IEZbZmE6ZmEtY2FyIENhcl0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ) a text description to diagram language
- SQL the standard database Structured Query Language
- HTML Hypertext Markup Language

> Surprising how many DSLs use acronyms for their name.

Some examples of how a DSL for data transformation can be useful in this process is by supporting a web interface for the data domain expert. The interface would allow matching incoming data columns with normalized data columns with a standardized transformation mapped between the two.

For example, Incoming *Table A, Column Weight* maps to Normalized *Table M, Column Weight* with a unit transformation from *pounds* to *kilograms*, which can be succinctly represented as `UnitConvert(A, from=”pounds”, to=”kilograms”).`

![](https://cdn-images-1.medium.com/max/800/1*eIbeJNixaFCnhFkA1cOt3A.png)

Using a DSL allows you to build a web or application interface to define all of the transformations for each new incoming database into the normalized format you need. Your domain expert doesn’t have to describe the transformations required into a specification document that your developers have to then interpret into code. Remember you’ll need up-to-date specifications for transforming each ***version*** of every ***source database***.

If you instead provide a system such that the healthcare data domain expert can define your data transformations in a nicely computable DSL format using an easy-to-use interface. *The exported DSL specification that the domain expert creates is immediately usable (as code!) for the data transformation process.* The specification (as DSL code) can also be easily versioned in a code repository since it is code. A DSL specification is very well defined compared to the written descriptions of transformations I’ve seen, and it doesn’t need re-interpretation by the developers requiring multiple cycles with the domain experts to figure out what they were trying to communicate.

> There may be a few instances of transformations that need to be customized to the incoming database and too hard to develop a DSL for. Those are easily handled as one-offs as they are not the bulk of the transformation process definition.

Another advantage of managing the transformation process like this is that the specifications can be partially automated and validated (e.g. a weight transformation should always result in kilograms or flag an error) while shared in a format that is easily understandable and curatable by both the domain expert and the developer(s) managing the data pipeline.

A final advantage is you also have a defined set of transformation functions defined in the DSL that you use over and over again and are easily regression tested for bugs. This is much better than multiple developers working on different transformation scripts for different databases which need to be tested separately.
