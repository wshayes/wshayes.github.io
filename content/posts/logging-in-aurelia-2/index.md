---
title: "Logging in Aurelia"
date: 2015-08-21T17:11:00.001Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

Just some quick notes on setting up logging in Aurelia

#### Add customer log appender

Create a file in ./resources/custom-log-appender.js and add the following class (or any other file as long as you change the import in the main.js file).

```
export class CustomLogAppender {  
  constructor(){}
  debug(logger, message, ...rest){
    console.debug(`DEBUG [${logger.id}] ${message}`, ...rest);
  }
  info(logger, message, ...rest){
    console.info(`INFO [${logger.id}] ${message}`, ...rest);
  }
  warn(logger, message, ...rest){
    console.warn(`WARN [${logger.id}] ${message}`, ...rest); 
  }
  error(logger, message, ...rest){
    console.error(`ERROR [${logger.id}] ${message}`, ...rest);
  }
}
```

#### Update your main.js

```
import {LogManager} from 'aurelia-framework';
import {CustomLogAppender} from './resources/custom-log-appender';

LogManager.addAppender(new CustomLogAppender());
LogManager.setLevel(LogManager.logLevel.debug);

export function configure(aurelia) {
  aurelia.use
    .standardConfiguration()
    // .developmentLogging()
    .plugin('aurelia-animator-css');

  aurelia.start().then(a => a.setRoot());
}
```

#### and in your View Model

```
# ViewModel
import {LogManager} from 'aurelia-framework';
let logger = LogManager.getLogger('viewmodulename');
logger.debug('me');

export class MyViewModel() {
  logger.info(“Hah”);
}
```
