import '../scss/critical.scss';
import '../scss/newamericadotorg.scss';
//import(/* webpackChunkName: "na-page-styles" */ '../scss/newamericadotorg.scss');

import 'babel-polyfill';
import 'whatwg-fetch';
import 'url-polyfill';
// import 'url-search-params-polyfill';

import reactRenderer from './react/react-renderer';
import actions from './react/actions';
import cache from './react/cache';

import addEventListeners from './add-event-listeners';
import addObservers from './add-observers';

// initialize on ready
if(document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

window.newamericadotorg = {
  react: reactRenderer,
  actions,
  cache
};

function init(){
  importPageComponents();
  addEventListeners();
  addObservers();
  actions.triggerScrollEvents();
  if(window.user.isAuthenticated){
    cache.clearAll();
    console.log('cache cleared');
  }
}

function importPageComponents(){
  import(/* webpackChunkName: "na-core-components" */ './react/components.core');

  switch(document.body.getAttribute('id')){
    case 'na-home':
      import(/* webpackChunkName: "na-home-components" */ './react/components.home');
      break;
    case 'na-program':
      import(/* webpackChunkName: "na-program-components" */ './react/components.program');
      break;
    case 'na-report':
      import(/* webpackChunkName: "na-report-components" */ './react/components.report');
      break;
    case 'na-weekly':
      import(/* webpackChunkName: "na-weekly-components" */ './react/components.weekly');
      break;
    case 'na-indepth':
      import(/* webpackChunkName: "na-indepth-components" */ './react/components.indepth');
      break;
    default:
      break;
  }
}
