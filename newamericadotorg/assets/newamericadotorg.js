import './scss/critical.scss';
import './scss/index.scss';

import React from 'react';
import ReactDOM from 'react-dom';
import * as ReactRedux from 'react-redux';
import * as Redux from 'redux';

window.React = React;
window.ReactDOM = ReactDOM;
window.ReactRedux = ReactRedux;
window.Redux = Redux;

import reactRenderer from './react/react-renderer';
import actions from './react/actions';
import cache from './react/cache';
import setMeta from './react/setMeta';
import addEventListeners from './lib/add-event-listeners';
import addObservers from './lib/add-observers';
import mobileMenu from './react/mobile-menu/index';
import Fetch from './react/api/components/Fetch';
import Response from './react/api/components/Response';

const _Fetch = props => (
  <ReactRedux.Provider store={store}>
    <Fetch {...props} />
  </ReactRedux.Provider>
);

const _Response = props => (
  <ReactRedux.Provider store={store}>
    <Response {...props} />
  </ReactRedux.Provider>
);

// initialize on ready
if (document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

window.newamericadotorg = {
  react: reactRenderer,
  actions,
  cache,
  Fetch: _Fetch,
  Response: _Response,
  renderDataViz: el => {
    let viz = document.querySelectorAll('.na-dataviz:not(.lazy)');

    if (!window.renderDataViz || !viz) return;
    for (let i = 0; i < viz.length; i++) {
      viz[i].setAttribute('id', viz[i].getAttribute('data-id'));
      window.renderDataViz(viz[i]);
    }
  }
};

function init() {
  setMeta();
  reactRenderer.add(mobileMenu);
  importPageComponents();
  addEventListeners();
  addObservers();
  actions.triggerScrollEvents();
  if (window.user.isAuthenticated) {
    cache.clearAll();
    console.log('cache cleared');
  }

  // JS for Datawrapper
  window.addEventListener("message",function(a){if(void 0!==a.data["datawrapper-height"])for(var e in a.data["datawrapper-height"]){var t=document.getElementById("datawrapper-chart-"+e)||document.querySelector("iframe[src*='"+e+"']");t&&(t.style.height=a.data["datawrapper-height"][e]+"px")}});
}

function importPageComponents() {
  import(/* webpackChunkName: "na-core-components" */ './react/components.core');

  switch (document.body.getAttribute('id')) {
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
