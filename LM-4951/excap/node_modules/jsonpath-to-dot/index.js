/**
 * @see https://tools.ietf.org/html/rfc6901#section-4
 * @param {string} path encoded JSON Pointer string
 * @returns {string} The object key.
 */
module.exports = function(path){
  return path.replace(/^\//, '').replace(/\//g, '.');
};
