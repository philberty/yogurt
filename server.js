#!/usr/bin/env node

var express = require ('express');
var app = express ();
 
app.get ('/', function(request, response) {
    response.sendfile ('public/index.html');
});

app.listen (3000);
