import $ from 'jquery'

function addSearchBoxInteraction() {
	$(".search-box__input")
		.on("focus", function() {
			var submit = $(this).siblings(".search-box__submit ");
			$(submit).children(".search-box__icon ").attr("fill", "#abacae");
		})
		.on("focusout", function() {
			var submit = $(this).siblings(".search-box__submit ");
			$(submit).children(".search-box__icon ").attr("fill", "#eaeaeb");
		});
}
$(addSearchBoxInteraction);