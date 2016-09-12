import $ from 'jquery';

export default function detectOverflow() {
	$(document).ready(setChartAreaWidth);
	$(window).resize(function() { setChartAreaWidth(); setOverflowPadding(); });
}

function setChartAreaWidth() {
	var bodyWidth = $("body").width();
	$(".chart-wrapper").css("max-width", bodyWidth - 100);
}

function setOverflowPadding() {
	$(".chart-wrapper").each( function() {
		var $chartWrapper = $(this);
		if ($chartWrapper.prop("offsetWidth") < $chartWrapper.prop("scrollWidth")) {
			$chartWrapper.css("padding-bottom", "15px");
		} else {
			$chartWrapper.css("padding-bottom", "0px");
		}
	});
	
}