import $ from 'jquery'

var navTemplate = require('./nav.jade')

$.fn.extend({

	/*
	 * Plug-in to animate border panels.
	 *
	 */
	startBorderPanel: function() {

		var width = 0
		var itemCount = 0
		var activeItemIndex = 0
		var $this = $(this)

		/*
		 * Entry point
		 */
		setup()
		addNav()
		addNavigationListeners()

		/*
		 * Cache element width and jQuery object.
		 *
		 */
		function setup() {
			activeItemIndex = 0
			itemCount = $this.find('.border-panel__item').length
			width = $this.width()
			update()
		}


		/*
		 *
		 *
		 */
		function addNav() {
			var navHtml = navTemplate({ buttonCount: itemCount })
			$this.prepend(navHtml)
		}


		/*
		 * Update dom.
		 *
		 */
		function update() {
			width = $this.width()

			$this.find('.border-panel__item').each((i, el) => {
				var $el = $(el)
				var xTransform = (i - activeItemIndex) * width
				$el.addTransformStyle(`translate(${xTransform}px, 0)`)
				$el.setModifier('border-panel__item', 'active', (i === activeItemIndex))
			})

			$this.find('.border-panel__button').each((i, el) => {
				$(el).setModifier('border-panel__button', 'active', (i === activeItemIndex))
			})
		}


		/*
		 * Adds nav click listeners
		 *
		 */
		function addNavigationListeners() {
			$this.find('.border-panel__nav').click((e) => { 
				var $target = $(e.target)
				if (!$target.hasClass('border-panel__button')) { return }
				var index = $target.index()
				if (activeItemIndex !== index) {
					activeItemIndex = index
					update()
				}			
			})
		}

	}

})

$(() => {
	$('.border-panel').each((i, el) => {
		$(el).startBorderPanel()
	})
})