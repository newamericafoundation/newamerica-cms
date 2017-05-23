/*

Primary Bundling Entry Point - imports scss files and all js modules and utilities

*/
import './../scss/newamericadotorg.scss';


//import './utilities/index.js';
// import modules from './modules/index.js';
import 'whatwg-fetch';
import * as React from 'react';

window.React = React;

import composer from './react-components/index';

const newamericadotorg = {
  composer
};

export default newamericadotorg;
