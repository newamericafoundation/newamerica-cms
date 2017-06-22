import './../scss/critical.scss';
import './../scss/newamericadotorg.scss';

import * as React from 'react';
import 'whatwg-fetch';
import 'url-polyfill';

window.React = React;

import composer from './react/index';
import { actions } from './react/actions';
import lazyload from './react/components/LazyLoad';

// initialize on ready
if(document.readyState != 'loading') init();
else document.addEventListener('DOMContentLoaded', init);

function init(){
  composer.init();
  actions.addScrollEvent({ selector: '.scroll-target' });
}

const newamericadotorg = {
  composer,
  lazyload,
  actions
};

export default newamericadotorg;
