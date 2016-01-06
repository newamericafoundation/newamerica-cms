import $ from 'jquery'

var formTemplate = require('./form.jade')

$(() => {

	const baseClass = 'subscribe'

	var $link = $(`#${baseClass}__link`)
	var $emailField = $(`#${baseClass}__email-field`)

	$link.on('click', () => {
		var value = $emailField[0].value
		console.log(value)
	})

})