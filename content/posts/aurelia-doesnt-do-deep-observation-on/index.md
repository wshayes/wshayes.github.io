---
title: "Aurelia doesn't do deep observation on objects - View string interpolation fun"
date: 2015-08-31T17:51:00Z
draft: true
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

Which is fine.  I’m really just writing this to remind myself of the approach that Jeremy Danyow (@jdanyow) shared with me.

**Symptom**: can’t print out a current state of an object with nested structure via:

```
${object | objectToString}
```

  

**Reason**:  Aurelia doesn’t deep observe all properties on an object

**Background:**  I was updating properties on an object and trying to view its current state using string interpolation in the Aurelia View, but the string interpolation view of the object wasn't updating even though I could see the object was being updated via the logger.  Jeremy told me what was happening and suggested the following workaround.

**Workaround**:

get object() {return JSON.stringify(this.\_object, null, 2);}
