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
		addNavigationListeners()
		setCarouselInterval()


		/*
		 *
		 *
		 */
		function stepActiveItemIndex() {
			activeItemIndex += 1
			if (activeItemIndex === itemCount) {
				activeItemIndex = 0
			}
		}


		/*
		 * Cache element width and jQuery object.
		 *
		 */
		function setup() {
			activeItemIndex = 0
			itemCount = $this.find('.border-panel__item').length
			width = $this.width()
			addNav()
			update()
		}


		/*
		 * Add navigation html.
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
			// Update element width.
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


		/*
		 *
		 *
		 */
		function setCarouselInterval() {
			if (itemCount === 1) { return }
			setInterval(() => {
				stepActiveItemIndex()
				update()
			}, 5500)
		}

	}

})

$(() => {
	$('.border-panel').each((i, el) => {
		$(el).startBorderPanel()
	})
})