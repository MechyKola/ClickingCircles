# NEAfrontendVuexVuetify
trying a frontend using vuex and vuetify

# nea_frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Run your tests
```
npm run test
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Heroku
Add
```
    "postinstall": "npm run build",
    "start": "node server.js"
``` 
to scripts in package.json scripts

and
```
    "express": "*",
```
to dependencies

add file server.js to root which contains
```
var express = require('express');
var path = require('path');
var serveStatic = require('serve-static');

app = express();
app.use(serveStatic(__dirname + "/dist"));

var port = process.env.PORT || 5000;
app.listen(port);

console.log('server started '+ port);
```
