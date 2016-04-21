import $ from 'jquery'

var pictureGridTextHeight = 300;
var pictureGridEntryHeight = 500;

var mediumBreakpoint = 640;

var mediumMediaQuery = window.matchMedia("(min-width: " + mediumBreakpoint + "px)");
// resizeMediaQuery.addListener(removePictureGridInteraction);
// removePictureGridInteraction(resizeMediaQuery);

function addPictureGridInteraction() {
	$(".picture-grid__entry__text-container").on("mouseover", function() {
		if (mediumMediaQuery.matches) {
			var overflow = this.scrollHeight - pictureGridTextHeight;
			if (overflow > 0) {
				// if (overflow > pictureGridTextHeight) {
				// 	overflow = pictureGridTextHeight;
				// } else {
				// 	overflow = overflow + 10;
				// }
				// $(this).children(".picture-grid__entry__text-fadeout").hide();
				
				// $(this).css("transform", "translateY(-" + overflow + "px)").css("height", this.scrollHeight - 25);
				$(this).children(".picture-grid__entry__text-fadeout").hide();
				$(this).css("transform", "translateY(-" + (pictureGridEntryHeight - pictureGridTextHeight) + "px)").css("height", pictureGridEntryHeight - 25);
			}
		}
	});

	$(".picture-grid__entry__text-container").on("mouseout", function() {
		if (mediumMediaQuery.matches) {
			$(this).css("transform", "translateY(0)").css("height", pictureGridTextHeight - 25);
			$(this).children(".picture-grid__entry__text-fadeout").show();
		}
	});
}

$(addPictureGridInteraction);

