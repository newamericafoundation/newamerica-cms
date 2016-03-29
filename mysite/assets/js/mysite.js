import './../scss/mysite.scss'

import 'babel-polyfill'

import './utilities/index.js'
import './modules/index.js'

import 'script!jquery'
import 'script!foundation-sites/dist/foundation.js'

$(document).ready(function() {
	$(document).foundation();
});
  console.log("initializing foundation");
