import $ from 'jquery';

/* 
 * Function to dynamically size program dropdown height to avoid cutoff - only necessary for fixed header
 *
 */
export default function setProgramDropdownHeight() {
	if (!$("body").hasClass("header--expanded")) {
		const $programDropdownContent = $("#program-dropdown-content");
		const $headerLinkGroupFadeout = $(".header__link-group__fadeout");
		const headerHeight = 72;

		$("#program-dropdown-toggle").on("mouseover", function() {
			var windowHeightMinusHeader = $(window).height() - headerHeight;
			var progDropdownHeight = $programDropdownContent.height();
			var progDropdownScrollHeight = $programDropdownContent.prop("scrollHeight");

			// checks for existing overflow and resets height to auto - handles case where previous height caused overflow, but future height might be tall enough to fit full content
			if (progDropdownScrollHeight > progDropdownHeight) {
				$programDropdownContent.height("auto").css("overflow-y", "none");
				progDropdownHeight = $programDropdownContent.height();
				$headerLinkGroupFadeout.hide();
			}

			// if dropdown content height is greater than window height, sets dropdown height and overflow
			if (progDropdownHeight > windowHeightMinusHeader) {
				$programDropdownContent.height(windowHeightMinusHeader - 15).css("overflow-y", "scroll");
				$headerLinkGroupFadeout.show();
			}
		})
	}
	
}