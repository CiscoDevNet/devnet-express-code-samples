# express-mongo-rest
Node.js package to create an express middleware for a mongo-backed, RESTful API

```
var express = require('express')
var expressMongoRest = require('express-mongo-rest')
var app = express()
app.use('/api/v1', expressMongoRest('mongodb://localhost:27017/mydb'))
var server = app.listen(3000, function () {
    console.log('Listening on Port', server.address().port)
})
```
The middleware is schema-agnostic, allowing any json document to be persisted and retrieved from mongo.

| Route            | Method | Notes                       |
| ---------------- | ------ | --------------------------- |
| /:collection     | GET    | Search the collection (uses [query-to-mongo](https://www.npmjs.com/package/query-to-mongo)) |
| /:collection     | POST   | Create a single document    |
| /:collection     | PUT    | Method Not Allowed          |
| /:collection     | PATCH  | Method Not Allowed          |
| /:collection     | DELETE | Remove all documents        |
| /:collection/:id | GET    | Retrieve a single document  |
| /:collection/:id | POST   | Method Not Allowed          |
| /:collection/:id | PUT    | Create or update a document |
| /:collection/:id | PATCH  | Update fields in a document (uses [jsonpatch-to-mongodb](https://www.npmjs.com/package/jsonpatch-to-mongodb)) |
| /:collection/:id | DELETE | Remove a single document    |

## API
### expressMongoRest(db, options)
Create an express middleware that implements a RESTful API.

#### options:
* **envelope** Return responses wrapped in a type envelope. This can be overriden per request by specifying an _envelope_ query parameter.
* **singularize** A function to change the collection name into it's singlur form (ie., 'users' becomes 'user'). Used when returning a envelope for a single instance. Default is [inflection.singularize](https://www.npmjs.com/package/inflection).

## Use
I wanted to make it extremely simple to start a mongo-backed rest server, so `npm start` starts one. The `server.js` script employs many best-practices for rest servers such as using https, gzip, and method overrides.

You can configure the following options in the .env file (uses [dotenv](https://www.npmjs.com/package/dotenv)):
* **DB** The url for the mongo database. Default is `mongodb://localhost:27017/express-rest-mongo`.
* **PORT** The port to listen on. Default is 3000.
* **PFX** Certificate, Private key and CA certficiates to use for SSL. Default is none.
* **KEY** Private key to use for SSL. Default is none.
* **CERT** Certificate, to use for SSL. Default is none.
If neither of PFX or a KEY/CERT pair are specified, a self-sigend certificate and key is generated.

### Querying documents
The query API (GET /:collection) uses a robust query syntax that interprets comparision operators (=, !=, >, <, >=, <=) in the query portion of the URL using [query-to-mongo](https://www.npmjs.com/package/query-to-mongo).

For example, the URL `https://localhost/api/v1/users?firstName=John&age>=21` would search the _users_ collection for any entries that have a _firstName_ of "John" and an _age_ greater than or equal to 21.

### Patching documents
The patch document API (PATCH /:collection/:id) will update fields within a document. The API expects a JSON patch payload as defined in [RFC 6902](https://tools.ietf.org/html/rfc6902). The API uses [jsonpatch-to-mongodb](https://www.npmjs.com/package/jsonpatch-to-mongodb) to interpret the patch.

An example patch using jQuery:
```
$.ajax('https://localhost/api/v1/users/2d0aa7b0-cf14-413e-9093-7bbba4f4b220', {
  method: 'PATCH',
  contentType: 'application/json',
  data: JSON.stringify([
    { op: 'replace', path: '/firstName', value: 'Johnathan' },
    { op: 'replace', path: '/age', value: 22 }
  ]),
  success: function (data, status, xhr) {...},
  error: function (xhr, status, err) {...}
})
```

### Returning result envelopes
The APIs that return results (all except DELETE) can be set to wrap those results in a type envelope; either server-wide by specifying the _envelope_ option when creating the middleware, or per request by including an _envelope_ query paramter in the URL.

The type envelope will use the singularized name of the collection. The singularizer can be specified using the _singularize_ option when creating the middleware. The default is [inflection.singularize](https://www.npmjs.com/package/inflection).

For example `https://localhost/api/v1/users/2d0aa7b0-cf14-413e-9093-7bbba4f4b220?envelope=true` returns:
```
{
  user: {
    id: '2d0aa7b0-cf14-413e-9093-7bbba4f4b220',
    firstName: 'John',
    age: 21
  }
}
```
and `https://localhost/api/v1/users/2d0aa7b0-cf14-413e-9093-7bbba4f4b220?envelope=false` returns:
```
{
  id: '2d0aa7b0-cf14-413e-9093-7bbba4f4b220',
  firstName: 'John',
  age: 21
}
```
The envelope for query results uses the collection name (and assumes it is plural); `https://localhost/api/v1/users?envelope=true` returns:
```
{
  users: [
    {
      id: '2d0aa7b0-cf14-413e-9093-7bbba4f4b220',
      firstName: 'John',
      age: 21
    },
    {
      id: 'abf445fd-04db-495e-82f7-77fbf369f7ee',
      firstName: 'Bob',
      age: 28
    }
  ]
}
```

### Best Practices
The server script was strongly influenced by [these](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api) [articles](http://blog.mwaysolutions.com/2014/06/05/10-best-practices-for-better-restful-api/) about best practices for RESTful APIs.

Here's the list of recommendations from those articles. Items not yet supported are ~~struck-through~~:

1.  Use nouns but no verbs
2.  GET method and query parameters should not alter the state
3.  Use SSL everywhere
4.  ~~Have great documentation~~
5.  Use plural nouns
6.  ~~Use sub-resources for relations~~
7.  ~~Provide a way to autoload related resource representations~~
8.  Use HTTP headers for serialization formats
9.  ~~Use HATEOAS~~
10. Provider filtering, sorting, field selection and paging for collections
    * Filtering
    * Sorting
    * Field selection
    * Paging
11. Version your API
12. Return something useful from POST, PATCH, & PUT requests
13. Handle Errors with HTTP status codes
    * Use HTTP status codes
    * ~~Use error payloads~~
14. Allow overriding HTTP method
15. Use JSON where possible, ~~XML only if you have to~~ _No application/xml support_
16. Pretty print by default & ensure gzip is supported
17. Don't use response envelopes by default
18. Consider using JSON for POST, PUT and PATCH request bodies _No application/x-www-form-urlencoded or multipart/form-data support_
19. ~~Provide useful response headers for rate limiting~~
20. ~~Use token based authentication, transported over OAuth2 where delegation is needed~~
21. ~~Include response headers that facilitate caching~~

## Todo
* Address more best-practices in 'server.js'
    * Add schama validation (swagger-spec? json-schema?)
    * Add swagger.io for api documentation.
    * Add user authentication and authorization to API access (node-oauth2-server?)
    * Add rate limiting (express-limiter?)
    * Add OAuth2 (node-oauth2-server?)
