import $ from 'jquery'

function addSearchBoxInteraction() {
	$(".search-box__input")
		.on("focus", function() {
			$(".search-box__icon").attr("fill", "#abacae");
			console.log("focused!!!!");
		})
		.on("focusout", function() {
			$(".search-box__icon").attr("fill", "#eaeaeb");
		});
}
$(addSearchBoxInteraction);