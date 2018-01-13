import './../scss/critical.scss';
import './../scss/newamericadotorg.scss';

import * as React from 'react';
import 'whatwg-fetch';
import 'url-polyfill';

window.React = window.react = React;

import composer from './react/index';
import actions from './react/actions';
import lazyload from './react/components/LazyLoad';

import addEventListeners from './add-event-listeners';
import addObservers from './add-observers';
import triggerScrollEvents from './utils/trigger-scroll-events';

// initialize on ready
if(document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

function init(){
  addEventListeners();
  addObservers();
  composer.init();
  triggerScrollEvents(window.scrollY, window.scrollY, 'FORWARD', composer.store.getState().site.scroll.events);
}

const newamericadotorg = {
  composer,
  lazyload,
  actions
};

export default newamericadotorg;
