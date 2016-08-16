/*

Exports mapped object of all module functions, called in assets/mysite.js

*/
export default [
  'border-panel',
  'sidemenu',
  'weekly-sidemenu',
  'post-body',
  'mobile-menu',
  'subscribe',
  'picture-grid',
  'search',
  'header',
  'content-controls',
  'story-excerpt-ellipsis',
  'in-depth',
  'fixed-banner',
].map((moduleName) => require(`./${moduleName}/index.js`).default);
