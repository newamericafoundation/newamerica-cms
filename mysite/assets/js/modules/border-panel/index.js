import $ from 'jquery'

import addBorderPanelInteractivity from './plugins/index.js'

function addAllBorderPanelsInteractivity() {
	$('.border-panel').each((i, el) => {
		addBorderPanelInteractivity($(el))
	})

	var maxHeight = findMaxHeight();
	$(".border-panel").height(maxHeight + 50);

	console.log(maxHeight);
	
}

function findMaxHeight() {
	var maxHeight = 0;
	$.each($('.border-panel__text'), function() {
		if (maxHeight < $(this).height()) {
			maxHeight = $(this).height();
		}
	});

	return maxHeight;
}

$(addAllBorderPanelsInteractivity)

$(window).resize(function(){
	var maxHeight = findMaxHeight();
	$(".border-panel").height(maxHeight + 50);
});