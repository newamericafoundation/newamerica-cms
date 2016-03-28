import './../scss/mysite.scss'

import 'babel-polyfill'


import './utilities/index.js'
import './modules/index.js'
// import jQuery, $ from 'jquery'
import 'script!jquery'
// import 'script!what-input'
import 'script!foundation-sites'


$(document).ready(function() {
	$(document).foundation();
});
  console.log("initializing foundation");
