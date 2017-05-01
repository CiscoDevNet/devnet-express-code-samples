#!/usr/bin/env node
var request = require('request');
var url = 'https://api.ciscospark.com/v1/messages';
var token = '{access token}';
var auth = 'Bearer ' + token;
var room_id = '{room_id}';
var message = 'Hello World';

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
    form: {'roomId': room_id, 'text': message}
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
