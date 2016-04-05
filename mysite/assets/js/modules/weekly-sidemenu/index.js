import $ from 'jquery'

import getJQueryObjects from './../../utilities/get_jquery_objects.js'

function weeklyHighlightActiveLink() {
	$('.weekly-sidemenu__sibling-list__link').each(function() {
		var link = $(this).prop('href');
		console.log(link);

		if (link == window.location.href) {
			console.log("adding active class");
			$(this).addClass('active');
		}

		// console.log(window.location.href);
		// if ($(this).prop('href') == window.location.href) {
		// 	console.log("adding active class");
		// 	$(this).addClass('active');
		// }
	});
}

$(weeklyHighlightActiveLink)