import $ from 'jquery'

import getJQueryObjects from './../../utilities/get_jquery_objects.js'

import {
  CONTAINER_CLASS_NAME,
  LINK_GROUP_CLASS_NAME,
  LINK_GROUP_CONTENT_CLASS_NAME
} from './constants.js'

function addHeaderInteractivity() {

	var { $body, $window, $wrapper, $header } = getJQueryObjects()

	var $mainNavItems = $header.find(`.${CONTAINER_CLASS_NAME}`)
	var $linkGroups = $header.find(`.${LINK_GROUP_CLASS_NAME}`)
	var $readProgressBar = $header.find(`.header__read-progress-bar`)

	var $search = $('.header__search')
	var $searchIcon = $('.header__search__icon')

	setExpandedState();
	addSearchClickListener();
	sizeReadProgressBarOnScroll();

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
			var ratio = scrollTop / (totalHeight - windowHeight)
			$readProgressBar.css('width', `${ratio * 100}%`)
		})
	}
	
}

$(addHeaderInteractivity)