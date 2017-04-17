#!/usr/bin/env node
var http = require('http');
var request = require('request');
console.log("Server Listening on 8000");
http.createServer(function(req,res) {
   res.writeHead(200);
   req.on('data', function(message) {
	   var obj = JSON.parse(message);
       var notification = [];
       notification[0] = obj.notifications[0].deviceId;
       notification[1] = obj.notifications[0].boundary;
       notification[2] = obj.notifications[0].locationMapHierarchy;
       if (notification[1] == "INSIDE") {
           postMsg(notification);
       }
   });
    req.on('end', function() { console.log(request.url); res.end();
   });
}).listen(8000);


function postMsg(notification) {
var url = 'https://api.ciscospark.com/v1/messages';
var token = 'MTEwYWE3MjctY2QyZS00NWViLTk0ZmUtZjE2YmM1NzYxZjAwMDA2NGM0OGItNmE3';
var auth = 'Bearer ' + token;
var room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjBkMjhlNjAtOTlkZS0xMWU2LWJjOTktZjUyYzY4ZTZjZjVh';
var text, len, i;
len = notification.length;
text = "";
for (i = 0; i < len; i++) {
    text += " " + notification[i] + " ";
}

// Set the headers
var headers = {
    'Authorization': auth,
    'Content-Type': 'application/json'
}
// configure the request
var options = {
    url: url,
    method: 'POST',
    headers: headers,
    form: {'roomId': room_id, 'text': text}
}
// start the request
request(options, function (error, response, body) {
    if (!error && response.statusCode == 200) {
        // Print out the response body
        var body = JSON.parse(body);
        console.log(JSON.stringify(body, null, 4));
    } else if (error) {
          console.log('Error: ' + error);
      }
})
}
