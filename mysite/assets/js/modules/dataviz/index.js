import $ from 'jquery';

export default function detectOverflow() {
	$(document).ready(setChartAreaWidth);
	$(window).resize(function() { setChartAreaWidth(); setOverflowPadding(); });
}

function setChartAreaWidth() {
	var bodyWidth = $("body").width();
	if (bodyWidth >= 640 ) {
		$(".chart-wrapper").css("max-width", bodyWidth - 100);
	} else {
		$(".chart-wrapper").css("max-width", bodyWidth - 50);
	}
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