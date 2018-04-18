import './../scss/critical.scss';
import './../scss/newamericadotorg.scss';

import 'babel-polyfill';
import * as React from 'react';
import 'whatwg-fetch';
import 'url-polyfill';
import 'url-search-params-polyfill';

window.React = window.react = React;

import composer from './react/index';
import actions from './react/actions';
import cache from './react/cache';

import addEventListeners from './add-event-listeners';
import addObservers from './add-observers';

// initialize on ready
if(document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

function init(){
  addEventListeners();
  addObservers();
  composer.init();
  actions.triggerScrollEvents();
  if(window.user_is_authenticated){
    cache.clearAll();
    console.log('cache cleared');
  }
}

const newamericadotorg = {
  composer,
  actions,
  cache
};

export default newamericadotorg;
