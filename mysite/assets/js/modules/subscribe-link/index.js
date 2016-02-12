import $ from 'jquery'

var formTemplate = require('./form.jade')

function addSubscribeLinkInteractivity() {

	const BASE_CLASS = 'subscribe'

	var $link = $(`#${BASE_CLASS}__link`)
	var $emailField = $(`#${BASE_CLASS}__email-field`)

	$link.on('click', () => {
		var value = $emailField[0].value
		console.log(value)
	})

}

$(addSubscribeLinkInteractivity)
