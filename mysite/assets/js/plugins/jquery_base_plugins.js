import $ from 'jquery'

$.fn.extend({

	addTransformStyle: function(transformString) {
		$(this).css({
			'-webkit-transform': transformString,
			'-ms-transform': transformString,
			'transform': transformString
		})
	},

	setModifier: function(baseClass, modifier, condition = true) {
		var modifier = `${baseClass}--${modifier}`
		var $el = $(this)
		if (condition) {
			$el.addClass(modifier)
		} else {
			$el.removeClass(modifier)
		}
	},

	toggleModifier: function(baseClass, modifier) {
		var modifier = `${baseClass}--${modifier}`
		var $el = $(this)
		if ($el.hasClass(modifier)) {
			$el.removeClass(modifier)
		} else {
			$el.addClass(modifier)
		}
	}

})