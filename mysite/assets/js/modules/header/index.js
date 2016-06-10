import $ from 'jquery';

export default function setProgramDropdownHeight() {
	if (!$("body").hasClass("header--expanded")) {
		$("#program-dropdown-toggle").on("mouseover", function() {
			var windowHeightMinusHeader = $(window).height() - 72;
			var progDropdownHeight = $("#program-dropdown-content").height();
			var progDropdownScrollHeight = $("#program-dropdown-content").prop("scrollHeight");

			console.log("window height: " + windowHeightMinusHeader);
			console.log("prog dropdown height: " + progDropdownHeight);
			console.log("prog dropdown scroll height: " + progDropdownScrollHeight);

			if (progDropdownScrollHeight > progDropdownHeight) {
				console.log("overflow!");
				$("#program-dropdown-content").height("auto").css("overflow-y", "none");
				progDropdownHeight = $("#program-dropdown-content").height();
			}

			if (progDropdownHeight > windowHeightMinusHeader) {
				console.log("prog dropdown height is greater!");
				$("#program-dropdown-content").height(windowHeightMinusHeader - 15).css("overflow-y", "scroll");

			}

		})
	}
	
}