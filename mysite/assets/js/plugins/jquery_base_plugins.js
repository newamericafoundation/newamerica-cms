import $ from 'jquery'

$.fn.extend({

	/*
	 * Adds vendor-specific inline transform styles.
	 * @param {string} transformString - Compiled transform string, e.g. all 0.5s ease-in-out.
	 */
	addTransformStyle: function(transformString) {
		$(this).css({
			'-webkit-transform': transformString,
			'-ms-transform': transformString,
			'transform': transformString
		})
	},

	/*
	 * Sets a BEM modifier class on the element.
	 * @param {string} modifier
	 * @param {boolean} condition - Whether the modifier should be added or removed. Defaults to true.
	 * @param {baseClass} - Base class that is modified. May be ommitted if the element is selected by the base class selector.
	 */
	setModifierClass: function(modifier, condition = true, baseClass) {
		var $el = $(this)
		baseClass = baseClass || $el.selector.slice(1)
		var modifierClassName = `${baseClass}--${modifier}`
		if (condition) {
			$el.addClass(modifierClassName)
		} else {
			$el.removeClass(modifierClassName)
		}
	},

	/*
	 * Toggles a BEM modifier class on the element.
	 * @param {string} modifier
	 * @param {string} baseClass - Base class that is modified. May be ommitted if the element is selected by the base class selector.
	 * Examples:
	 *   - $('.header').toggleModifierClass('active') toggles the header--active modifier.
	 *   - $('#other-selector').toggleModifierClass('active', 'header'), does the same thing, but the 'header' argument may not be ommitted.
	 */
	toggleModifierClass: function(modifier, baseClass) {
		var $el = $(this)
		baseClass = baseClass || $el.selector.slice(1)
		var modifierClassName = `${baseClass}--${modifier}`
		if ($el.hasClass(modifierClassName)) {
			$el.removeClass(modifierClassName)
		} else {
			$el.addClass(modifierClassName)
		}
	}

})
