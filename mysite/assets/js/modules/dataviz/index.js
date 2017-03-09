import $ from 'jquery';

var browser = require('detect-browser');

import domtoimage from 'dom-to-image';

var printWidth = 725;

export default function() {
	$(document).ready(function() {
		setChartWrapperWidth(); 
		addChartButtonInteractivity(); 
	});
	$(window).resize(function() { 
		setChartWrapperWidth(); 
		setChartWrapperOverflowPadding(); 
	});
}

function setChartWrapperWidth() {
	var bodyWidth = $("body").width();
	if (bodyWidth >= 640 ) {
		$(".chart-wrapper").css("max-width", bodyWidth - 100);
	} else {
		$(".chart-wrapper").css("max-width", bodyWidth - 50);
	}
}

function setChartWrapperOverflowPadding() {
	$(".chart-wrapper").each( function() {
		var $chartWrapper = $(this);
		if ($chartWrapper.prop("offsetWidth") < $chartWrapper.prop("scrollWidth")) {
			$chartWrapper.css("padding-bottom", "15px");
		} else {
			$chartWrapper.css("padding-bottom", "0px");
		}
	});
}

function addChartButtonInteractivity() {
	$(".dataviz").each(function(index, item) {
		var $item = $(item);
		var chartArea = $item.find(".dataviz__chart-area")[0];
		var downloadLink = $item.find(".dataviz__download-link");
		var embedLink = $item.find(".dataviz__embed-link");
		var shareLink = $item.find(".dataviz__share-link");
		var embedPopup = $item.find(".dataviz__embed-popup");
		var sharePopup = $item.find(".dataviz__share-popup");
		
		downloadLink.click(function() { handleDownloadClickEvent(chartArea) });
		embedLink.click(function() { embedPopup.toggle(); });
		shareLink.click(function() { sharePopup.toggle(); });

		$('body').click(function(evt){
			if(evt.target.class == "dataviz__share-popup" || evt.target.class == ".dataviz__share-link" || evt.target.class == "dataviz__embed-popup" || evt.target.class == ".dataviz__embed-link")
				return;
			// excepts descendents of share link and share popup
			if($(evt.target).closest('.dataviz__share-popup').length || $(evt.target).closest('.dataviz__share-link').length || $(evt.target).closest('.dataviz__embed-popup').length || $(evt.target).closest('.dataviz__embed-link').length)
				return; 

			embedPopup.hide();
			sharePopup.hide();
		});

		addShareIcons(sharePopup);

		// hides download links on Internet Explorer
		hideDownloadLink(downloadLink);

		// addEmbedInteractivity(embedLink, chartArea);
		// addShareInteractivity(shareLink, chartArea);
	});
}

function handleDownloadClickEvent(chartArea) {
	domtoimage.toPng(chartArea)
	    .then((dataUrl) => {
	    	var id = $(chartArea).attr("id");
			var link = document.createElement("a");
		    link.download = id + '.png';
		    link.href = dataUrl;
		    link.click();
		    link.remove();
	    })
	    .catch(function (error) {
	        console.error('oops, something went wrong!', error);
	    });
}



// hides download links on Internet Explorer and shows alternative download data message
function hideDownloadLink(downloadLink) {
	if (browser.name == "ie") {
		$(downloadLink).hide();
		$(".in-depth__footer__download-data-message").show();
	} else if (browser.name == "safari") {
		$(".in-depth__footer__download-data-message").show();
	}
}

// adds click toggle handlers to share popup 
// function addShareInteractivity(shareLink, chartArea) {
// 	var popup = $(shareLink).siblings(".dataviz__share-popup");
// 	$(shareLink).click(function() { popup.toggle(); });

// 	$('body').click(function(evt){
// 		if(evt.target.class == "dataviz__share-popup" || evt.target.class == ".dataviz__share-link")
// 			return;
// 		// excepts descendents of share link and share popup
// 		if($(evt.target).closest('.dataviz__share-popup').length || $(evt.target).closest('.dataviz__share-link').length)
// 			return; 

// 		$(".dataviz__share-popup").hide();
// 	});
// 	addShareIcons(popup);
// }


function addShareIcons(popup) {
	var urlPieces = window.location.href.split("#");
	var currUrl = urlPieces[0];
	var title = popup.siblings(".dataviz__title").text();
	var anchor = popup.siblings(".in-depth__panel__anchor").attr("id");

	popup.jsSocials({
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