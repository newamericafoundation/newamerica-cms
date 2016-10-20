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
		var chartArea = $(item).find(".dataviz__chart-area")[0];
		var downloadLink = $(item).find(".dataviz__download-link");
		var printLink = $(item).find(".dataviz__print-link");
		var shareLink = $(item).find(".dataviz__share-link");
		
		downloadLink.click(function() { handlePrintDownloadClickEvent("download", chartArea) });
		printLink.click(function() { handlePrintDownloadClickEvent("print", chartArea) });

		// hides print and download links on Internet Explorer
		hidePrintDownloadLinks(downloadLink, printLink);

		addShareInteractivity(shareLink, chartArea);
	});
}

function handlePrintDownloadClickEvent(eventType, chartArea) {
	domtoimage.toPng(chartArea)
	    .then((dataUrl) => {
	    	if (eventType == "download") {
	    		downloadChart(dataUrl, chartArea);
	    	} else {
	    		printChart(dataUrl, chartArea);
	    	}
	    })
	    .catch(function (error) {
	        console.error('oops, something went wrong!', error);
	    });
}

function downloadChart(dataUrl, chartArea) {
	var id = $(chartArea).attr("id");
	var link = document.createElement("a");
    link.download = id + '.png';
    link.href = dataUrl;
    link.click();
    link.remove();
}

function printChart(dataUrl, chartArea) {
	var currWidth = $(chartArea).width();
	var currHeight = $(chartArea).height();
	var aspect = currHeight/currWidth;

    var adjustedHeight = ( printWidth * aspect) + "px";
    var popup = window.open();
	popup.document.write("<img src=" + dataUrl + " height=" + adjustedHeight + " width=" + printWidth + "px></img>");
	popup.focus(); //required for IE
	popup.print();
}

// hides download links on Internet Explorer and shows alternative download data message
function hidePrintDownloadLinks(downloadLink, printLink) {
	if (browser.name == "ie") {
		$(downloadLink).hide();
		$(printLink).hide();
		$(".in-depth__footer__download-data-message").show();
	} else if (browser.name == "safari") {
		$(".in-depth__footer__download-data-message").show();
	}
}

// adds click toggle handlers to share popup 
function addShareInteractivity(shareLink, chartArea) {
	var popup = $(shareLink).siblings(".dataviz__share-popup");
	$(shareLink).click(function() { popup.toggle(); });

	$('body').click(function(evt){
		if(evt.target.class == "dataviz__share-popup" || evt.target.class == ".dataviz__share-link")
			return;
		// excepts descendents of share link and share popup
		if($(evt.target).closest('.dataviz__share-popup').length || $(evt.target).closest('.dataviz__share-link').length)
			return; 

		$(".dataviz__share-popup").hide();
	});
	addShareIcons(popup);
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