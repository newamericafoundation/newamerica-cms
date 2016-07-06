import $ from 'jquery'
/*


*/

export default function() {
	addSectionHeaderInteraction();
	inDepthPanelScroll();

}

function addSectionHeaderInteraction() {
	Foundation.MediaQuery.get('desktop-header')
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
					breakpoint: 1024,
					settings: {
						slidesToShow: 2,
					}
			    },
			    {
					breakpoint: 1200,
					settings: {
						slidesToShow: 3,
					}
			    }
			]
		}).on('afterChange', toggleArrowDisplay);

		//
		toggleArrowDisplay();
	});
}

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

function resizeTitlePanelBackground() {
	
	$(document).ready(function(){
		setTitlePanelBackgroundOverflow();
	});

	$(window).resize(function(){
		setTitlePanelBackgroundOverflow();
	});
}

function setTitlePanelBackgroundOverflow() {
	var maxSiteWidth = 1350;

	var $windowWidth = $(window).width();
	if ($windowWidth > maxSiteWidth) {
		var overflow = ($windowWidth - maxSiteWidth)/2 + 25;
		console.log(overflow);
		$(".title-panel").css("margin-left", overflow * -1).css("margin-right", overflow * -1).css("padding-left", overflow).css("padding-right", overflow);
	}
}

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
    //smooth scroll to second section
    $('.cd-scroll-down').on('click', function(event){
        event.preventDefault();
        smoothScroll($(this.hash));
    });

    //open-close navigation on touch devices
    $('.touch .cd-nav-trigger').on('click', function(){
    	$('.touch #cd-vertical-nav').toggleClass('open');
  
    });
    //close navigation on touch devices when selectin an elemnt from the list
    $('.touch #cd-vertical-nav a').on('click', function(){
    	$('.touch #cd-vertical-nav').removeClass('open');
    });

	function updateNavigation() {
		contentSections.each(function(){
			var $this = $(this);
			var activeSection = $('#cd-vertical-nav a[href="#'+$this.attr('id')+'"]').data('number') - 1;
			if ( ( $this.offset().top - $(window).height()/2 < $(window).scrollTop() ) && ( $this.offset().top + $this.height() - $(window).height()/2 > $(window).scrollTop() ) ) {
				navigationItems.eq(activeSection).addClass('is-selected');
			}else {
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