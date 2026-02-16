---
title: "Dynamic input list in Aurelia"
date: 2015-08-30T00:46:00.002Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I struggled with getting this dynamic form pattern figured out in [Aurelia](http://aurelia.io/) so I'm sharing it here for myself in the future and others that might find it useful.  
  
The features needed are:  

- Automatically add new blank input fields at the end of the list as needed
- Allow the removal of any items from the list at any point
- Allow changing any items in the list of inputs

  
Given lots of help from the [Aurelia Gitter channel](http://gitter.im/Aurelia/Discuss) especially by Jeremy Danyow (@jdanyow) and Io Sulfur (@iosulfur) who created several Plunkrs zeroing in on the right solution, we came up with this approach as demonstrated in the Plunkr below.  
  
Anytime you change the blank item field at the end, it will add another empty input field at the end. If you click on the 'X' button, it will remove that item.
  

## [Demo Plunkr](http://plnkr.co/edit/Gp7wV3?p=preview)

The key things to note in the app.html listing below are that the 'items' in line 6 must be your actual array.  If this is in a nested repeat.for loop and items is made available from the parent repeat.for, this approach will not update the original array only the one that is local to the repeat.for context.  
  
The change.delegate on line 8 adds the blank line using the current index value of the repeat and the change event.  You'll see how they are used in the app.js file below.  
  
The click.delegate very simply removes the input field by splicing out that item from the items array.  
  

### app.html

{{% gist wshayes 5042098006898c34ad42 %}}

  
The first thing to do is to add a blank item at the end of the items array before we even present it to the View in line 7 of app.js  
  
The addBlank function first sets the current item (based on the $index value passed from the change.delegate function) to the event.target.value and then blanks out the event.target.value.  We blank out the event.target.value as otherwise that value gets added to the end of the list of input fields.  
  
We then check to see if the last input field is empty or not, and if it returns true, we push an empty string onto items.  (Note: if anyone can explain why you get the event.target.value instead of the empty '' string unless we reset the event.target.value, please post it in the comments - because I've not been able to figure it out.   
  
The removeItem is pretty self-explanatory - so that's all.  Thanks for reading, hope it is useful.  
  
Added (2015-08-30) :  When I tried this with an object as the item, I didn't need lines 12 and 13 in app.js.  
  

### app.js

{{% gist wshayes cf79a2512ab82a1185fd %}}
