import $ from 'jquery'

// import getJQueryObjects from './../../utilities/get_jquery_objects.js'

// import {
//   CONTAINER_CLASS_NAME,
//   LINK_GROUP_CLASS_NAME,
//   LINK_GROUP_CONTENT_CLASS_NAME
// } from './constants.js'

var desktopHeaderBreakpoint = 945;

var headerExpanded = false;
var sidemenuExpanded = false;

function addMenuResponsivity() {
	$(".header__mobile-toggle__button").on("click", function() {
		// toggle arrow for header, ensure arrow up for sidemenu
		$(this).children(".rotate").toggleClass("down");
		$(".mobile-sidemenu__toggle__button").children(".rotate").removeClass("down");

		// toggle header menu and ensure sidemenu hidden
		$(".mobile-header").toggle();
		$(".sidemenu").css("display", "none");
		sidemenuExpanded = false;

		// if expanding header, hide content and footer, else show content and footer
		if (headerExpanded) {
			$(".content-container").css("display", "table-cell");
			$("footer").css("display", "block");
			headerExpanded = false;
		} else {
			$(".content-container").css("display", "none");
			$("footer").css("display", "none");
			headerExpanded = true;
		}
		
	})

	$(".mobile-sidemenu__toggle__button").on("click", function() {
		// toggle arrow for sidemenu, ensure arrow up for header
		$(this).children(".rotate").toggleClass("down");
		$(".header__mobile-toggle__button").children(".rotate").removeClass("down");

		$(".sidemenu").toggle();
		$(".mobile-header").css("display", "none");
		headerExpanded = false;
		// sidemenuExpanded = !sidemenuExpanded;

		if (sidemenuExpanded) {
			$(".content-container").css("display", "table-cell");
			$("footer").css("display", "block");
			sidemenuExpanded = false;
		} else {
			$(".content-container").css("display", "none");
			$("footer").css("display", "none");
			sidemenuExpanded = true;
		}
	})


	// $(".rotate").on("click", function () {
	// 	console.log("toggling down class");
	//     $(this).toggleClass("down");
	// })
}

$(addMenuResponsivity);


var $window = $( window ); // so you have a "cached" reference 
// var breakpoint = 640;

$window.resize ( function () {
	// console.log("calling resize");
		if ($window.width() > desktopHeaderBreakpoint ) {
			// if (clicked == true ) {
				console.log("width is greater");
				$(".mobile-sidemenu").css("display", "none");
		    	$(".sidemenu").css("display", "block");
		    	$(".mobile-header").css("display", "none");
				$(".content-container").css("display", "table-cell");
				$("footer").css("display", "block");
				sidemenuExpanded = false;
				headerExpanded = false;
				// clicked = false;
			
	  	} else {
	  		$(".mobile-sidemenu").css("display", "block");

	  		if (!sidemenuExpanded) {
	  			$(".sidemenu").css("display", "none");
	  		}
	  		if (!headerExpanded) {
	  			$(".mobile-header").css("display", "none");
	  		}
	  	} 
	
});