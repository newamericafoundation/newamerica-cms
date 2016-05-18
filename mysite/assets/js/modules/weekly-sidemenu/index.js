import $ from 'jquery';
/*

Highlights active link in the sidemenu on weekly article pages by comparing the current window location url to all
	hrefs in the weekly sidemenu sibling list

*/
export default function weeklyHighlightActiveLink() {
	$('.weekly__sidemenu__sibling-list__link').each(function() {
		const link = $(this).prop('href');
		if (link === window.location.href) {
			$(this).addClass('active');
		}
	});
}
