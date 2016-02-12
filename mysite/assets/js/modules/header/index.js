import $ from 'jquery'

function isEscape(keyCode) {
	return (keyCode === 27)
}

function addHeaderInteractivity() {

	const CONTAINER_CLASS_NAME = 'header__has-link-group'
	const LINK_GROUP_CLASS_NAME = 'header__link-group'
	const LINK_GROUP_CONTENT_CLASS_NAME = 'header__link-group__content'

	var $body = $(document.body)
	var $window = $(window)

	var $wrapper = $('.wrapper')

	var $header = $('.header')
	var $mainNavItems = $header.find(`.${CONTAINER_CLASS_NAME}`)
	var $linkGroups = $header.find(`.${LINK_GROUP_CLASS_NAME}`)
	var $readProgressBar = $header.find(`.header__read-progress-bar`)

	var $search = $('.header__search')
	var $searchIcon = $('.header__search__icon')

	setExpandedState()
	addSearchClickListener()
	closeMainNavItemsOnEscape()
	sizeReadProgressBarOnScroll()

	function closeMainNavItemsOnEscape() {
		$body.on('keydown', (e) => {
			if (isEscape(e.keyCode)) {
				$mainNavItems.setModifierClass('active', false, CONTAINER_CLASS_NAME)
			}
		})
	}

	function setExpandedState() {
		var isExpanded = window.uiState ? window.uiState.isHeaderExpanded : false
		$body.setModifierClass('expanded', isExpanded, 'header')
	}

	function addSearchClickListener() {
		$searchIcon.on('click', () => {
			$search.toggleModifierClass('active', 'header__search')
		})
	}

	function sizeReadProgressBarOnScroll() {
		$window.on('scroll', (e) => {
			var scrollTop = $body.scrollTop()
			var totalHeight = $wrapper.height()
			var windowHeight = $window.height()
			console.log(scrollTop, totalHeight, windowHeight)
			var ratio = scrollTop / (totalHeight - windowHeight)
			console.log(ratio)
			$readProgressBar.css('width', `${ratio * 100}%`)
		})
	}

}

$(addHeaderInteractivity)
