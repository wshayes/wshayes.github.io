---
title: "Aurelia, Firefox and Input fields"
date: 2016-01-15T12:42:00Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I had a mis-behaving checkbox input field on Firefox.  The checkbox was working fine on Chrome and Safari - likely IE as well.  But it wouldn't stay checked on Firefox - kept resetting itself to unchecked.  For the short version, @jsobell on Aurelia's Gitter channel told me that Firefox triggers input attributes based on alphabetical order.  I had a model.bind(), checked.bind(), and change.trigger() on the checkbox in question in that order.  The change.trigger() was running last with the other browsers and first in Firefox.   
  
It was sloppy code on my part, I should have processed everything in the change.trigger function instead of a kludge of model.bind and checked.bind with a change.trigger that was really carrying the main functionality.
