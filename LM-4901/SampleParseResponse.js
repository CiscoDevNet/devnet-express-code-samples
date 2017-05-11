#!/usr/bin/env node
var http = require('http');
console.log("Server Listening on 8000");
http.createServer(function(request,response) {
   response.writeHead(200);
   request.on('data', function(message) {
	   var obj = JSON.parse(message);
	   console.log("deviceId: ",obj.notifications[0].deviceId);
	   console.log("boundary: ",obj.notifications[0].boundary);
	   console.log("locationMapHierarchy: ",
                                obj.notifications[0].locationMapHierarchy);
   });
   request.on('end', function() { console.log(request.url); response.end();
   });
}).listen(8000);
