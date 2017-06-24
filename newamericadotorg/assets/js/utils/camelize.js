/**
  Return camelCase version of-a-string
**/

const camelize = function(str) {
  return str.replace(/(?:^\w|[A-Z]|\b\w)/g, function(letter, index) {
    return index == 0 ? letter.toLowerCase() : letter.toUpperCase();
  }).replace(/\s+/g, '').replace('-','');
}

export default camelize;
