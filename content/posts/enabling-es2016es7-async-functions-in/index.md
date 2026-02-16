---
title: "Enabling ES2016(ES7) Async functions in Aurelia"
date: 2015-08-18T16:40:00.001Z
tags: ["WebDev", "Aurelia"]
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I was having a lot of problems getting the Javascript ES2016 (ES7) async functions working in Aurelia. I knew I had to update the config.js code in Aurelia by adding *es7.asyncFunctions*:

```
System.config({  
  defaultJSExtensions: true,  
  transpiler: "babel",  
  babelOptions: {  
    "optional": [  
      "es7.decorators",  
      "es7.classProperties",  
      "es7.asyncFunctions",  
      "runtime"  
    ]  
  },
```

I then tried to add my async method function to an Aurelia ViewModel:

```
async activate () {  
  try {  
    this.results = await this.api.search();  
    console.log(`Search results: ${this.results.evidence}`);  
  }  
  catch (err) {  
    console.log(err);  
  }  
}
```

and promptly got this error in my javascript console after the page loaded:

```
ERROR [app-router] ReferenceError: regeneratorRuntime is not defined
```

Jeff Bellsey (@jbellsey) on Gitter -> Aurelia/Discuss was kind enough to figure out the issue and share it with me.  I was not however smart enough to understand the answer at the time. He told me I had to add the runtime to the babel-options file **(/build/babel-options.js)**:

```
module.exports = {  
  modules: 'system',  
  moduleIds: false,  
  comments: false,  
  compact: false,  
  stage:2,  
  optional: [  
    "es7.decorators",  
    "es7.classProperties",  
    "es7.asyncFunctions",  
    "runtime"  
  ]  
};
```

The “runtime” and “es7.asyncFunctions” lines need to be added to the file.

This was a LOT of fun to sort out.  However, I now have, for me, much more understandable code using the async, try, await, catch format.  Thank you Jeff and the other fantastic Aurelians!

```
 
```
