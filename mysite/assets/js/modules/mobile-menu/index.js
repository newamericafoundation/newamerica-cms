import $ from 'jquery';

export default function menuToggle(){
	$('.mobile-nav__main').click(function(){
		$(this).toggleClass('active-nav')
			.siblings().removeClass('active-nav');

		$('body')
			.toggleClass('mobile-menu--expanded')
			.removeClass('secondary-menu--expanded');
	});

	$('.mobile-nav__secondary').click(function(){
		$(this).toggleClass('active-nav')
			.siblings().removeClass('active-nav');

		$('body')
			.toggleClass('secondary-menu--expanded')
			.removeClass('mobile-menu--expanded');
	});

	$('.mobile-menu__link__main a').click(function() {
		$(this).parent().toggleClass('active-nav');
	});

}
