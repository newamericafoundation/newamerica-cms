import './../scss/newamericadotorg.scss';

// import modules from './modules/index.js';
import * as React from 'react';
import 'whatwg-fetch';

window.React = React;

import composer from './react-components/index';
import { actions } from './react-components/events';
import lazyload from './react-components/lazyload';

const newamericadotorg = {
  composer,
  lazyload,
  actions
};

export default newamericadotorg;
