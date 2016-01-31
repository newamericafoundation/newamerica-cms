import $ from 'jquery'

function addHeaderInteractivity() {

	const NAV_ITEM_CLASS_NAME = 'header__main-nav__item'
	const NAV_ITEM_LINK_GROUP_CLASS_NAME = 'header__link-group'

	var $header = $('.header')
	var $body = $(document.body)
	var $mainNavItems = $header.find(`.${NAV_ITEM_CLASS_NAME}`)

	setExpandedState()
	addNavItemListeners()

	function setExpandedState() {
		var isExpanded = window.uiState ? window.uiState.isHeaderExpanded : false
		$body.setModifier('header', 'expanded', isExpanded)
	}

	function addNavItemListeners() {
		$mainNavItems.on('click', (e) => {
			var $target = $(e.currentTarget)
			var $linkGroup = $target.find(`.${NAV_ITEM_LINK_GROUP_CLASS_NAME}`)
			if ($linkGroup.length > 0) {
				e.preventDefault()
				$target.toggleModifier(NAV_ITEM_CLASS_NAME, 'active')
			}
		})
	}

}

$(addHeaderInteractivity)