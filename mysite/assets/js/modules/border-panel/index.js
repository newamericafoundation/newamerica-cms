import $ from 'jquery';

import addBorderPanelInteractivity from './plugins/index.js';

export default function addAllBorderPanelsInteractivity() {
	$('.border-panel').each((i, el) => {
		addBorderPanelInteractivity($(el))
	})

	var maxHeight = findMaxHeight();
	setBorderPanelHeight(maxHeight);

	$(window).resize(function(){
		var maxHeight = findMaxHeight();
		setBorderPanelHeight(maxHeight);
	});
}

function findMaxHeight() {
	var maxHeight = 0;
	$.each($('.border-panel__item'), function() {
		var height = $(this).find(".border-panel__text").height();

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

function setBorderPanelHeight(maxHeight) {
	if ($(window).width() > 640) {
		$(".border-panel").height(maxHeight + 50);
	} else {
		$(".border-panel").height(maxHeight + 10);
	}
}
