#!/usr/bin/env node

var http = require('http');

console.log("Server Listening on 8000");
http.createServer(function(request,response) {
   response.writeHead(200);
   request.on('data', function(message) {
       console.log(message.toString());
       response.write(message);
   });

   request.on('end', function() {
       console.log(request.url);
       response.end();
   });
}).listen(8000);
