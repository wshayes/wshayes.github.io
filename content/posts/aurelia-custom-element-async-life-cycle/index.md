---
title: "Aurelia custom element async life cycle event"
date: 2016-03-17T22:57:00.002Z
tags: ["Aurelia"]
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I saw a really good conversation in the Aurelia/framework Github issue queue that I wanted to save for later.  <https://github.com/aurelia/framework/issues/367#issuecomment-198104416>  
  
From Rob Eisenberg:  
  
> We can't provide this (async promise life-cycle events) across all components. It would be a disaster for performance and would no longer map in any way to web components.

> If you don't care about web components, you can use the new CompositionTransaction: <http://aurelia.io/docs.html#/aurelia/templating/1.0.0-beta.1.1.2/doc/api/class/CompositionTransaction>

> Simply have that injected into your component constructor and then call enlist() this will return you a CompositionTransactionNotifier: <http://aurelia.io/docs.html#/aurelia/templating/1.0.0-beta.1.1.2/doc/api/interface/CompositionTransactionNotifier>

> You can call done on that when your async operation is complete. The global composition will wait to attach until after you are done.

  
**How do I wait for async data for an Aurelia custom element?**  
  
  

{{% gist wshayes 775ec6cef36eb5b2be8a %}}
