import $ from 'jquery'

var OTIurl = "oti";

function checkOTI() {
	var url = window.location.href;
	var urlPieces = url.split('/');
	for (var i in urlPieces) {
		if (urlPieces[i].toLowerCase() === OTIurl) {
			$(".wrapper").addClass("oti");
		}
	}
}

$( document ).ready(function() {
	$(checkOTI);
});