import $ from 'jquery'

import getJQueryObjects from './../../utilities/get_jquery_objects.js'

function weeklyHighlightActiveLink() {
	$('.weekly-sidemenu__sibling-list__link').each(function() {
		var link = $(this).prop('href');

		if (link == window.location.href) {
			$(this).addClass('active');
		}
	});
}

$(weeklyHighlightActiveLink)