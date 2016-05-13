/*

Exports mapped object of all module functions, called in assets/mysite.js

*/
export default [
  'border-panel',
  'header',
  'sidemenu',
  'weekly-sidemenu',
  'post-body',
  'mobile-menu',
  'oti',
  'subscribe',
  'picture-grid',
  'search',
  'content-controls',
  'story-excerpt-ellipsis'
].map((moduleName) => require(`./${moduleName}/index.js`).default);
