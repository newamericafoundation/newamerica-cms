import './../scss/newamericadotorg.scss';

// import modules from './modules/index.js';
import * as React from 'react';
import 'whatwg-fetch';
import 'url-polyfill';

window.React = React;

import composer from './react/index';
import { actions } from './react/actions';
import lazyload from './react/components/LazyLoad';

const newamericadotorg = {
  composer,
  lazyload,
  actions
};

export default newamericadotorg;
