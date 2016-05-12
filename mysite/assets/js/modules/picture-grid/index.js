import $ from 'jquery'
/*

Adds hover interaction to shift picture grid text box to full height of grid entry.
	Only in effect past the medium breakpoint 

*/

var mediumBreakpoint = 640;
var mediumMediaQuery = window.matchMedia("(min-width: " + mediumBreakpoint + "px)");

export default function addPictureGridInteraction() {
	var pictureGridTextHeight = 300;
	var pictureGridEntryHeight = 500;

	$(".picture-grid__entry__text-container.has-image").on("mouseover", function() {
		if (mediumMediaQuery.matches) {
			var overflow = this.scrollHeight - pictureGridTextHeight;
			if (overflow > 0) {
				$(this).children(".picture-grid__entry__text-fadeout").hide();
				$(this).css("transform", "translateY(-" + (pictureGridEntryHeight - pictureGridTextHeight) + "px)").css("height", pictureGridEntryHeight - 25);
			}
		}
	});

	$(".picture-grid__entry__text-container.has-image").on("mouseout", function() {
		if (mediumMediaQuery.matches) {
			$(this).css("transform", "translateY(0)").css("height", pictureGridTextHeight - 25);
			$(this).children(".picture-grid__entry__text-fadeout").show();
		}
	});
}
