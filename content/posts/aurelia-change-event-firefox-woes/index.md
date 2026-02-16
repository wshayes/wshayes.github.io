---
title: "Aurelia change event Firefox woes"
date: 2016-03-02T18:52:00.001Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

In the continuing adventures of Firefox vs other browsers (see [Aurelia Firefox and Input fields](http://blog.williamhayes.org/2016/01/aurelia-firefox-and-input-fields.html)), I was watching a checkbox using a **change.trigger()**to update the checkbox selection state for a search facet.  I noticed in Firefox that the change event checkbox selection value was pre-change vs Chrome and other browsers where the selection value was post-change.   
  
[Gitter Aurelia conversation](https://gitter.im/Aurelia/Discuss?at=5639d129a530033014e41607) discussed the issue and approach to fix it.  
  

{{% gist wshayes d9f0b8b6b92efa532959 %}}

Using change.delegate gives the change event time to finish processing before it's handled.  I'm a little concerned about timing issues still as this doesn't seem deterministic, but it's working pretty well now.
