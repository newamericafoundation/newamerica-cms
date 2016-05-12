import $ from 'jquery';

import getJQueryObjects from './../../utilities/get_jquery_objects.js';

import {
  CONTAINER_CLASS_NAME,
  LINK_GROUP_CLASS_NAME
} from './constants.js';

/*

Sets expanded body class based on window ui-state

*/
export default function addHeaderInteractivity() {

	var { $body, $window } = getJQueryObjects();

	setExpandedState();

	function setExpandedState() {
		var isExpanded = window.uiState ? window.uiState.isHeaderExpanded : false
		$body.setModifierClass('expanded', isExpanded, 'header')
	}

}
