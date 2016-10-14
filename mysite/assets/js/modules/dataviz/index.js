import $ from 'jquery';

export default function detectOverflow() {
	$(document).ready(setChartAreaWidth);
	$(document).ready(addDownloadPopupInteractivity);
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

function addDownloadPopupInteractivity() {
	$(".dataviz__download-link").each(function(index, item) {
		console.log(item);
		$(item).on("click", function() {
			var popup = $(item).siblings(".dataviz__download-popup");
			popup.toggle();
		})

		$('body').click(function(evt){
			console.log(evt.target);  
			if(evt.target.class == "dataviz__download-popup" || evt.target.class == "dataviz__download-link")
				return;
			// excepts descendents of download link and download popup
			if($(evt.target).closest('.dataviz__download-popup').length || $(evt.target).closest('.dataviz__download-link').length)
				return; 

			$(".dataviz__download-popup").hide();
		});

	})
}