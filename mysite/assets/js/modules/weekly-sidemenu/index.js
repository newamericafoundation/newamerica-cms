import $ from 'jquery';

export default function weeklyHighlightActiveLink() {
	$('.weekly-sidemenu__sibling-list__link').each(function() {
		const link = $(this).prop('href');
		if (link === window.location.href) {
			$(this).addClass('active');
		}
	});
}
