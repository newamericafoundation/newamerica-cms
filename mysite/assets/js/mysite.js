import './../scss/mysite.scss'

import 'babel-polyfill'

import $ from 'jquery'

import './plugins/index.js'

import './modules/border-panel/index.js'
import './modules/subscribe-link/index.js'

// Entry point to the app.
function startNewAmerica() {
	console.log('Hi, Mom!')
}

$(startNewAmerica)