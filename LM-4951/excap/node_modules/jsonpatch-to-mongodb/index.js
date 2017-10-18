var toDot = require('jsonpath-to-dot');

module.exports = function(patches){
  var update = {};
  patches.map(function(p){
    if(p.op === 'add'){
      var path = toDot(p.path);
      if(!update.$push) update.$push = {};
      if(!update.$push[path]) {
        update.$push[path] = p.value;
      } else if (update.$push[path]) {
        if(!update.$push[path].$each) {
          update.$push[path] = {$each : [update.$push[path]]};
        }
        update.$push[path].$each.push(p.value);
      }
    }
    else if(p.op === 'remove'){
      if(!update.$unset) update.$unset = {};
      update.$unset[toDot(p.path)] = 1;
    }
    else if(p.op === 'replace'){
      if(!update.$set) update.$set = {};
      update.$set[toDot(p.path)] = p.value;
    }
    else if(p.op !== 'test') {
      throw new Error('Unsupported Operation! op = ' + p.op);
    }
  });
  return update;
};
