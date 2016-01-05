import $ from 'jquery'

$.fn.extend({

	/*
	 * Plug-in to animate border panels.
	 *
	 */
	animateBorderPanel: function() {

		var width = 0
		var itemCount = 0
		var activeItemIndex = 0
		var $this = $(this)

		/*
		 * Entry point
		 */
		setup()
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
		 * Update dom.
		 *
		 */
		function update() {
			width = $this.width()

			$this.find('.border-panel__item').each((i, el) => {
				var $el = $(el)
				console.log(i, activeItemIndex)
				var xTransform = (i - activeItemIndex) * width
				if (i === activeItemIndex) {
					$el.addClass('border-panel__item--active')
				} else {
					$el.removeClass('border-panel__item--active')
				}
				$el.css('transform', `translate(${xTransform}px, 0)`)
			})

			$this.find('.border-panel__button').each((i, el) => {
				var $el = $(el)
				if (i === activeItemIndex) {
					$el.addClass('border-panel__button--active')
				} else {
					$el.removeClass('border-panel__button--active')
				}
			})
		}


		/*
		 *
		 *
		 */
		function addNavigationListeners() {
			$this.find('.border-panel__nav').click((e) => { 
				var $target = $(e.target)
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
		$(el).animateBorderPanel()
	})
})