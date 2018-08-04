/**
  Return camelCase version of-a-string
**/

const camelize = function(str) {
  return str.replace(/-([a-z])/g, function(g){return g[1].toUpperCase(); });;
}

export default camelize;
