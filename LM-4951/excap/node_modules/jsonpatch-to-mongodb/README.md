# jsonpatch-to-mongodb

[![build status](https://secure.travis-ci.org/mongodb-js/jsonpatch-to-mongodb.png)](http://travis-ci.org/mongodb-js/jsonpatch-to-mongodb)

Convert [JSON patches](http://jsonpatch.com/) into a MongoDB update.

## Example

```javascript
var toMongodb = require('jsonpatch-to-mongodb');
var patches = [{
  op: 'replace',
  path: '/name',
  value: 'dave'
}];

console.log(toMongodb(patches));
// {'$set': {name: 'dave'}};
```

Example: [with express and mongoose](http://github.com/imlucas/jsonpatch-to-mongodb/tree/master/examples/express)


## Install

```
npm install --save jsonpatch-to-mongodb
```

## Test

```
npm test
```

## License

MIT
