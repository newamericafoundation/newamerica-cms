import $ from 'jquery';

import addBorderPanelInteractivity from './plugins/index.js';

/*

Iterates through border panel elements calling add interactivity function
	- calls function to find max height of any border panel element
	- calls function to set height of border panels to max height
	- adds resize listener to change border panel heights to adapt for text wrapping

*/

export default function addAllBorderPanelsInteractivity() {
	$('.border-panel').each((i, el) => {
		addBorderPanelInteractivity($(el))
	})

	$(document).ready(function(){
		var maxHeight = findMaxHeight();
		$(".border-panel").height(maxHeight + 50);
	});

	$(window).resize(function(){
		var maxHeight = findMaxHeight();
		$(".border-panel").height(maxHeight + 50);
	});
}

/*

Iterates through border panel items, calculating max text height

*/
function findMaxHeight() {
	var maxHeight = 0;
	$.each($('.border-panel__item'), function() {
		var height = $(this).find(".border-panel__text").height();
		// if border panel has circle nav ( > 1 child) adds extra padding to account for added height
		if (!$(this).parent(".border-panel__list").hasClass("has-1-children")) {
			height = height + 40;
		} else {
			height = height + 20;
		}
		if (maxHeight < height) {
			maxHeight = height;
		}
	});

	return maxHeight;
}