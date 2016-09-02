import $ from 'jquery';

export default function detectOverflow() {
	$(document).ready(setChartAreaWidth);

	$(window).resize(setChartAreaWidth);
}

function setChartAreaWidth() {
	var bodyWidth = $("body").width();
	$(".chart-wrapper").css("max-width", bodyWidth - 50);

	console.log($(".chart-wrapper").scrollWidth);
	if ($(".dataviz__chart-wrapper").offsetWidth < $(".dataviz__chart-wrapper").scrollWidth) {
		console.log("overflowing!!!");
	}
}