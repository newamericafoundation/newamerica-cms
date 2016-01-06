import $ from 'jquery'

$.fn.extend({

	/*
	 * Adds prefixed transform style.
	 *
	 */
	addTransformStyle: function(transformString) {
		$(this).css({
			'-webkit-transform': transformString,
			'-ms-transform': transformString,
			'transform': transformString
		})
	},


	/*
	 * Sets BEM modifier class.
	 *
	 */
	setModifier: function(baseClass, modifier, condition) {
		var modifier = `${baseClass}--${modifier}`
		var $el = $(this)
		if (condition) {
			$el.addClass(modifier)
		} else {
			$el.removeClass(modifier)
		}
	}

})