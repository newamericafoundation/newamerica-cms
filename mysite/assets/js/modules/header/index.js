import $ from 'jquery'

function addLinkGroupInteractivity() {

	const CONTAINER_CLASS_NAME = 'header__has-link-group'
	const LINK_GROUP_CLASS_NAME = 'header__link-group'
	const LINK_GROUP_CONTENT_CLASS_NAME = 'header__link-group__content'

	var $header = $('.header')
	var $body = $(document.body)
	var $mainNavItems = $header.find(`.${CONTAINER_CLASS_NAME}`)
	var $linkGroups = $header.find(`.${LINK_GROUP_CLASS_NAME}`)

	setExpandedState()
	addNavItemListeners()

	function isEscape(keyCode) { return (keyCode === 27) }

	$(document.body).on('keydown', (e) => {
		if (isEscape(e.keyCode)) {
			$mainNavItems.setModifier(CONTAINER_CLASS_NAME, 'active', false)
		}
	})

	function setExpandedState() {
		var isExpanded = window.uiState ? window.uiState.isHeaderExpanded : false
		$body.setModifier('header', 'expanded', isExpanded)
	}

	function addNavItemListeners() {
		$mainNavItems.on('click', (e) => {

			var $currentTarget = $(e.currentTarget)
			var $target = $(e.target)
			var $linkGroup = $target.find(`.${LINK_GROUP_CLASS_NAME}`)
			var isTargetParentOfLinkGroup = $linkGroup.length > 0

			$currentTarget.setModifier(CONTAINER_CLASS_NAME, 'active', !$target.hasClass(LINK_GROUP_CLASS_NAME))

		})

	}

}

$(addLinkGroupInteractivity)