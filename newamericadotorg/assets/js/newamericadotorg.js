import './../scss/newamericadotorg.scss';

// import modules from './modules/index.js';
import * as React from 'react';
import 'whatwg-fetch';

window.React = React;

import composer from './react-components/index';
import lazyload from './utils/lazyload';

const newamericadotorg = {
  composer,
  lazyload
};

export default newamericadotorg;
