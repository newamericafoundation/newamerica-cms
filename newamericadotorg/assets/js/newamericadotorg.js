import './../scss/newamericadotorg.scss';

// import modules from './modules/index.js';
import * as React from 'react';
import 'whatwg-fetch';

window.React = React;

import composer from './react-components/index';
import { events } from './react-components/events';
import lazyload from './utils/lazyload';

const newamericadotorg = {
  composer,
  lazyload,
  events
};

export default newamericadotorg;
