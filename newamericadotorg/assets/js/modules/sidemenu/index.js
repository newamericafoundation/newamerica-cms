import $ from 'jquery';

import getJQueryObjects from './../../utilities/get_jquery_objects.js';

/*

Highlights active link in sidemenu by comparing current window location url to hrefs of all links and sublinks in sidemenu
	- toggles sub list items if parent is active
	- toggles parent list item if sub list item is active

*/
export default function highlightActiveLink() {

	$('.sidemenu__link-group__link').each(function() {
		if ($(this).children("a").prop('href') == window.location.href.split("?")[0]) {
			$(this).children("a").addClass('active');

			if($(this).hasClass('has-sublinks')) {
				showSublinks($(this).children(".sidemenu__sub-link-group"));
			}
		}
	});

	$('.sidemenu__sub-link-group__sub-link').each(function() {

		if ($(this).children("a").prop('href') == window.location.href.split("?")[0]) {
			$(this).children("a").addClass('active');
			showSublinks($(this).parent(".sidemenu__sub-link-group"));
		}
	});

	function showSublinks(sublinkGroup) {
		$(sublinkGroup).show();
	}
}