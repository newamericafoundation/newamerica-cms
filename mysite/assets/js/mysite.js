/*

Primary Bundling Entry Point - imports scss files and all js modules and utilities

*/
import './../scss/mysite.scss';

import 'babel-polyfill';

import './utilities/index.js';
import modules from './modules/index.js';

import $ from 'jquery';
import moment from 'moment';


global.$ = $;
global.jQuery = $;
global.moment = moment;

require('../vendor/jssocials.min.js');

$(document).ready(function() {
	require('../vendor/jquery-ui.min.js');
	require('../vendor/jquery.comiseo.daterangepicker.min.js');
	require('foundation-sites');
	$(document).foundation();
	getHeaderBreakpoints();
	modules.forEach((module) => {
		module();
	});
});

function getHeaderBreakpoints() {
	global.headerBreakpoints = {
		desktopHeader: Foundation.MediaQuery.get('desktop-header'),
		expandedHeader: Foundation.MediaQuery.get('expanded-header'),
	}
}
