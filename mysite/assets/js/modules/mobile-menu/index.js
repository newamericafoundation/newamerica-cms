import $ from 'jquery';

export default function menuToggle(){
	$('.mobile-nav__main').click(function(){
		$('body').toggleClass('mobile-menu--expanded')
			.removeClass('secondary-menu--expanded');
	});

	$('.mobile-nav__secondary').click(function(){
		$('body').toggleClass('secondary-menu--expanded')
			.removeClass('mobile-menu--expanded');
	});

	addMobileMenuArrowInteraction()
}

function addMobileMenuArrowInteraction() {
	$('.mobile-menu__link__main a')
		.on('click', function() {
			$(this).siblings('.rotate').toggleClass('down');
		});

	// sets fill change for secondary menu arrows on hover
	$('.mobile-header .mobile-menu__link__main a')
		.on('mouseover', function() {
			$(this).siblings('.rotate').removeClass('flip-arrow-black').addClass('flip-arrow-white');
		})
		.on('mouseout', function() {
			$(this).siblings('.rotate').removeClass('flip-arrow-white').addClass('flip-arrow-black');
		});
}
