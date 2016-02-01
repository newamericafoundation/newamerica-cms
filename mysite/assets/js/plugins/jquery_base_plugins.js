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
		var modifierClassName = `${baseClass}--${modifier}`
		var $el = $(this)
		if (condition) {
			$el.addClass(modifierClassName)
		} else {
			$el.removeClass(modifierClassName)
		}
	},

	toggleModifier: function(baseClass, modifier) {
		var modifierClassName = `${baseClass}--${modifier}`
		var $el = $(this)
		if ($el.hasClass(modifierClassName)) {
			$el.removeClass(modifierClassName)
		} else {
			$el.addClass(modifierClassName)
		}
	}

})