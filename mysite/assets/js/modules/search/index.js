import $ from 'jquery'
/*

Changes fill of search box icon when search box is focused and adds override to ensure mobile search box can be submitted on enter

*/
export default function addSearchBoxInteraction() {
	$(".search-box__input")
		.on("focus", function() {
			var submit = $(this).siblings(".search-box__submit ");
			$(submit).children(".search-box__icon ").attr("fill", "#abacae");
		})
		.on("focusout", function() {
			var submit = $(this).siblings(".search-box__submit ");
			$(submit).children(".search-box__icon ").attr("fill", "#eaeaeb");
		});

	// override to allow mobile menu search bar to be submitted on enter keystroke
	$('.mobile-header .search-box').keydown(function(e) {
		var key = e.which;
		// ASCII code for ENTER key is "13"
		if (key == 13) {
			$(this).submit(); // Submit form code
		}
	});
}
