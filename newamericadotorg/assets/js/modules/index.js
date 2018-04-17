/*

Exports mapped object of all module functions, called in assets/newamericadotorg.js

*/
export default [
  'border-panel',
  'post-body',
  'subscribe',
  'in-depth',
  'dataviz',
  'conference',
  'timeline'
].map((moduleName) => require(`./${moduleName}/index.js`).default);
