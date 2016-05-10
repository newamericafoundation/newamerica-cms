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
  'content-controls'
].map((moduleName) => require(`./${moduleName}/index.js`).default);
