import $ from 'jquery'

var pictureGridTextHeight = 300;

function addPictureGridInteraction() {
	$(".picture-grid__entry__text-container").on("mouseover", function() {
		var overflow = this.scrollHeight - pictureGridTextHeight;
		if (overflow > 0) {
			if (overflow > pictureGridTextHeight) {
				overflow = pictureGridTextHeight;
			} else {
				overflow = overflow + 10;
			}
			
			$(this).css("transform", "translateY(-" + overflow + "px)").css("overflow", "visible");
		}

	});

	$(".picture-grid__entry__text-container").on("mouseout", function() {
		$(this).css("transform", "translateY(0)").css("overflow", "hidden");
	});
}

$( document ).ready(function() {
	$(addPictureGridInteraction);
});