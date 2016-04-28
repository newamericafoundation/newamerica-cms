import $ from 'jquery'

import getJQueryObjects from './../../utilities/get_jquery_objects.js'

function highlightActiveLink() {

	$('.sidemenu__link-group__link').each(function() {
		
		if ($(this).children("a").prop('href') == window.location.href) {
			$(this).children("a").addClass('active');
			
			if($(this).hasClass('has-sublinks')) {
				showSublinks($(this).children(".sidemenu__sub-link-group"));
			}
		}
	});

	$('.sidemenu__sub-link-group__sub-link').each(function() {

		if ($(this).children("a").prop('href') == window.location.href) {
			$(this).children("a").addClass('active');
			showSublinks($(this).parent(".sidemenu__sub-link-group"));
		}
	});

	function showSublinks(sublinkGroup) {
		$(sublinkGroup).show();
	}
}

$( document ).ready(function() {
	$(highlightActiveLink)
});

// var clicked = false;

// function addSidemenuInteractivity() {
// 	$(".mobile-sidemenu__toggle").on("click", function() {
// 		clicked = !clicked;
// 		console.log("clicked!");
// 		$(".sidemenu").toggle();
// 		$(".content-container").toggle();
// 		$("footer").toggle();
// 	})
// }

// $(addSidemenuInteractivity)

// var $window = $( window ); // so you have a "cached" reference 
// var breakpoint = 640;

// $window.resize ( function () {
// 	// console.log("calling resize");
// 		if ($window.width() > breakpoint ) {
// 			// if (clicked == true ) {
// 				// console.log("width is greater");
// 		    	$(".sidemenu").css("display", "block");
// 				$(".content-container").css("display", "table-cell");
// 				$("footer").css("display", "block");
// 				clicked = false;
			
// 	  	} else {
// 	  		if (!clicked) {
// 	  			$(".sidemenu").css("display", "none");
// 	  		}
// 	  	} 
	
// });

