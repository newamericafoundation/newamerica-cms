import $ from 'jquery'

var navTemplate = require('./nav.jade')

$.fn.extend({

	addBorderPanelInteractivity: function() {

		const INTERVAL = 5500

		const CONTENT_ITEM_CLASS_NAME = 'border-panel__item'
		const NAV_CLASS_NAME = 'nav-circles'
		const NAV_ITEM_CLASS_NAME = 'nav-circles__circle'

		const LEFT_ARROW_CLASS_NAME = 'border-panel__arrow-nav__left'
		const RIGHT_ARROW_CLASS_NAME = 'border-panel__arrow-nav__right'

		var width = 0
		var itemCount = 0
		var activeItemIndex = 0
		var $this = $(this)

		var shouldChangeOnInterval = true

		start()

		function start() {
			setup()
			addNavigationListeners()
			setCarouselInterval()
		}

		function shiftActiveItemIndex(step = +1) {
			activeItemIndex += step
			if (activeItemIndex >= itemCount) {
				activeItemIndex = 0
			} else if (activeItemIndex <= -1) {
				activeItemIndex = itemCount - 1
			}
		}

		function setup() {
			activeItemIndex = 0
			itemCount = $this.find(`.${CONTENT_ITEM_CLASS_NAME}`).length
			width = $this.width()
			addNav()
			update()
		}

		function addNav() {
			var navHtml = navTemplate({ buttonCount: itemCount })
			$this.prepend(navHtml)
		}

		function update() {
			// Update element width.
			width = $this.width()

			$this.find(`.${CONTENT_ITEM_CLASS_NAME}`).each((i, el) => {
				var $el = $(el)
				var xTransform = (i - activeItemIndex) * width
				$el.addTransformStyle(`translate(${xTransform}px, 0)`)
				$el.setModifier(CONTENT_ITEM_CLASS_NAME, 'active', (i === activeItemIndex))
			})

			$this.find(`.${NAV_ITEM_CLASS_NAME}`).each((i, el) => {
				$(el).setModifier(NAV_ITEM_CLASS_NAME, 'active', (i === activeItemIndex))
			})
		}

		function addNavigationListeners() {
			$this.find(`.${NAV_CLASS_NAME}`).click((e) => { 
				var $target = $(e.target)
				shouldChangeOnInterval = false
				if (!$target.hasClass(NAV_ITEM_CLASS_NAME)) { return }
				var index = $target.index()
				if (activeItemIndex !== index) {
					activeItemIndex = index
					update()
				}
			})

			$this.find(`.${LEFT_ARROW_CLASS_NAME}`).click((e) => {
				shiftActiveItemIndex(-1)
				shouldChangeOnInterval = false
				update()
			})

			$this.find(`.${RIGHT_ARROW_CLASS_NAME}`).click((e) => {
				shiftActiveItemIndex(+1)
				shouldChangeOnInterval = false
				update()
			})

		}

		function setCarouselInterval() {
			if (itemCount === 1) { return }
			setInterval(() => {
				if (!shouldChangeOnInterval) {
					shouldChangeOnInterval = true
					return
				}
				shiftActiveItemIndex(+1)
				update()
			}, INTERVAL)
		}

	}

})

$(() => {
	$('.border-panel').each((i, el) => {
		$(el).addBorderPanelInteractivity()
	})
})