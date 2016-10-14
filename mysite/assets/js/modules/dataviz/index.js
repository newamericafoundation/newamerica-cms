import $ from 'jquery';

export default function detectOverflow() {
	$(document).ready(setChartAreaWidth);
	$(document).ready(addSharePopupInteractivity);
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

function addSharePopupInteractivity() {
	$(".dataviz__share-link").each(function(index, item) {
		// console.log(item);
		var popup = $(item).siblings(".dataviz__share-popup");
		$(item).on("click", function() {
			popup.toggle();
		})

		$('body').click(function(evt){
			if(evt.target.class == "dataviz__share-popup" || evt.target.class == ".dataviz__share-link")
				return;
			// excepts descendents of share link and share popup
			if($(evt.target).closest('.dataviz__share-popup').length || $(evt.target).closest('.dataviz__share-link').length)
				return; 

			$(".dataviz__share-popup").hide();
		});

		addShareIcons(popup);

	})
}

function addShareIcons(popup) {
	var urlPieces = window.location.href.split("#");
	var currUrl = urlPieces[0];
	var title = $(popup).siblings(".dataviz__title").text();
	var anchor = $(popup).siblings(".in-depth__panel__anchor").attr("id");

	$(popup).jsSocials({
		url: currUrl + "#" + anchor,
    	showCount: true,
		showLabel: true,
		text: title,
		shareIn: "popup",
        shares: [
        	{
        		share: "email",
	        	label: "Email",
			    logo: "fa fa-envelope",
			}, 
			"twitter",
			{
				share: "facebook",
			    label: "Share",
			    logo: "fa fa-facebook"
			}]
    });
}