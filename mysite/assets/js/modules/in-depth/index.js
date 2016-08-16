import $ from 'jquery'
/*
	in-depth/index.js - adds in-depth section header interaction, 
		- implements slick carousel - documentation: http://kenwheeler.github.io/slick/

*/

export default function() {
	addSectionHeaderInteraction();
	inDepthPanelScroll();
}

/*

	Implements slick carousel for in-depth section header, adds event listener and calls initially 
		helper function to toggle carousel arrows on scroll

*/
function addSectionHeaderInteraction() {
	$(document).ready(function(){
		$('.in-depth__section__header__item-container').slick({
			prevArrow: ".in-depth__section__header__arrow__previous",
			nextArrow: ".in-depth__section__header__arrow__next",
			infinite: false,
			swipeToSlide: true,
			slidesToShow: 1,
			mobileFirst: true,
			responsive: [
				{
					breakpoint: 1023,
					settings: {
						slidesToShow: 2,
					}
			    },
			    {
					breakpoint: 1199,
					settings: {
						slidesToShow: 3,
					}
			    }
			]
		}).on('afterChange', toggleArrowDisplay);

		// calls helper function on page load to show/hide scroll arrows
		toggleArrowDisplay();
	});
}

/*

	Helper function that shows/hides carousel arrows if at either end of carousel options

*/
function toggleArrowDisplay() {
	var $firstChild = $(".in-depth__section__header__item:first-child");
	var $lastChild = $(".in-depth__section__header__item:last-child");

	if ($firstChild.hasClass("slick-active")) {
		$(".in-depth__section__header__arrow__previous").hide();
	} else {
		$(".in-depth__section__header__arrow__previous").show();
	}

	if ($lastChild.hasClass("slick-active")) {
		$(".in-depth__section__header__arrow__next").hide();
	} else {
		$(".in-depth__section__header__arrow__next").show();
	}
}

/*

	Implements vertical fixed navigation interaction on scroll - using code from/based off of example 
		found here: https://codyhouse.co/gem/vertical-fixed-navigation/

*/

function inDepthPanelScroll() {
	var contentSections = $('.in-depth__panel'),
		navigationItems = $('#cd-vertical-nav a');
	updateNavigation();
	$(window).on('scroll', function(){
		updateNavigation();
	});

	//smooth scroll to the section
	navigationItems.on('click', function(event){
        event.preventDefault();
        smoothScroll($(this.hash));
    });

    //open-close navigation on touch devices
    $('.touch .cd-nav-trigger').on('click', function(){
    	$('.touch #cd-vertical-nav').toggleClass('open');
    });
    //close navigation on touch devices when selecting an element from the list
    $('.touch #cd-vertical-nav a').on('click', function(){
    	$('.touch #cd-vertical-nav').removeClass('open');
    });

    $('.title-panel__scroll-down').on('click', function(event){
        event.preventDefault();
        smoothScroll($(this.hash));
    });

	function updateNavigation() {
		contentSections.each(function(){
			var $this = $(this);
			var activeSection = $('#cd-vertical-nav a[href="#'+$this.attr('id')+'"]').data('number');
			if ( ( $this.offset().top - $(window).height()/2 < $(window).scrollTop() ) && ( $this.offset().top + $this.height() - $(window).height()/2 > $(window).scrollTop() ) ) {
				navigationItems.eq(activeSection).addClass('is-selected');
			} else {
				navigationItems.eq(activeSection).removeClass('is-selected');
			}
		});
	}

	function smoothScroll(target) {
        $('body,html').animate(
        	{'scrollTop':target.offset().top},
        	600
        );
	}
}