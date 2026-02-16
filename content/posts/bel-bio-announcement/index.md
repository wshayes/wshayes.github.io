---
title: "BEL.bio Announcement"
date: 2018-01-31T15:56:53.055Z
categories: ["Medium Archive"]
---

---

![Photo by Michał Parzuchowski on Unsplash](1EvGHSWmpzrknJVczHXsyiw.jpeg)
*Photo by Michał Parzuchowski on Unsplash*

We have developed the [BEL.bio](http://bel.bio) tools and resources to make working with BEL 2.0+ easier. The goals of developing a new [BEL (Biological Expression Language)](http://bel-api.readthedocs.io/en/latest/glossary.html) platform are:

- Simplify the BEL infrastructure and tooling
- Allow for faster BEL Language evolution
- Ability to simultaneously handle multiple versions of BEL
- More efficient BEL resource (BEL Namespaces, orthology, etc) mgmt

Feedback regarding OpenBEL tooling and infrastructure was unanimous in that the BEL Community was not interested in developing with Ruby/JRuby to further develop the OpenBEL Platform. Further, administering and maintaining the OpenBEL platform was more difficult than expected. With ideas and lessons learned gleaned from OpenBEL, we moved forward with a complete rewrite from the ground up.

### BEL.bio Platform

A completely redesigned BEL Platform, called BEL.bio due to the use of [bel.bio](http://bel.bio) as the domain name, has been developed over the last year after gathering feedback from many groups involved in BEL. High points of the platform are:

- Python-based platform, which is more familiar to the BEL community
- [BEL Language Specification file](https://github.com/belbio/bel/blob/master/bel/lang/versions/bel_v2_0_0.yaml) for each version of BEL that drives syntactic and semantic validation, BEL completion, etc
- Integrates with GraphDati NanopubStore, EdgeStore and NetworkStore for high-level data stores for BEL Nanopubs, BEL Edges and BEL Networks
- Integrates with [Elasticsearch](https://www.elastic.co/) for BEL Namespace searches for fast, flexible and advanced search/completion functionality
- Integrates with [ArangoDB](https://www.arangodb.com/) for BEL Namespace equivalencing and orthologization as graph database queries
- [BEL.bio API](http://bel-api.readthedocs.io) provides REST API access to BEL.bio functionality useful for analytics and integration
- [BEL Python package](https://pypi.org/project/bel/) that powers much of the functionality of the BEL.bio API and provides a command line interface for running ad hoc commands

### Your Review and Feedback

There is still much work to be done, but there is now enough functional and documented capability to solicit feedback on whether the choices we have made to this point are valid and useful to the community.

- [BEL.bio API documentation](http://bel-api.readthedocs.io/en/latest/)
- [BEL.bio API Live Swagger](http://apidocs.bel.bio/)
- [BEL python module documentation](http://bel.readthedocs.io/en/latest/)
- [BEL Resources documentation](http://bel-resources.readthedocs.io/en/latest/)
- [Github organization for BEL.bio](https://github.com/belbio)
- [Waffleboard overview of Github BEL.bio tasks/issues](https://waffle.io/belbio/project)

Please either share issues you find with BEL.bio in Github in the relevant repository or feel free to share your thoughts in the [OpenBEL Discussion Group](https://groups.google.com/forum/#!forum/openbel-discuss) which we are involved in. We welcome your insight as well as code contributions!
