import $ from 'jquery'

var OTIurl = "oti";

function checkOTI() {
	var url = window.location.href;
	var urlPieces = url.split('/');
	for (var i in urlPieces) {
		if (urlPieces[i].toLowerCase() === OTIurl) {
			console.log("in oti!");
			$(".wrapper").addClass("oti");
		}
	}
	console.log(urlPieces);
}

$(checkOTI);