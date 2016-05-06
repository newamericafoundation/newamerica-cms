import $ from 'jquery'

var maxLength = 140;

//
// catch for legacy content with cut off story excerpts - adds ellipsis to any story excerpt appearing in the content grids or picture grids
//
function addAllStoryExcerptEllipsis() {
	function addEllipsis() {
		var text = $(this).text();
		if (text.length >= maxLength) {
			$(this).text(text + "...");
		}
	}

	$(".content-entry__text__excerpt").each(addEllipsis);
	$(".picture-grid__entry__body").each(addEllipsis);
}

$(addAllStoryExcerptEllipsis);