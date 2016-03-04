import $ from 'jquery'

// import getJQueryObjects from './../../utilities/get_jquery_objects.js'

// import {
//   CONTAINER_CLASS_NAME,
//   LINK_GROUP_CLASS_NAME,
//   LINK_GROUP_CONTENT_CLASS_NAME
// } from './constants.js'

var headerExpanded = false;
var sidemenuExpanded = false;

function addMenuResponsivity() {
	$(".header__mobile-toggle__button").on("click", function() {
		$(".mobile-header").toggle();
		// $(".mobile-sidemenu").toggle();
		$(".sidemenu").css("display", "none");
		sidemenuExpanded = false;

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
		sidemenuExpanded = !sidemenuExpanded;
		console.log("clicked!");
		$(".sidemenu").toggle();
		$(".content-container").toggle();
		$("footer").toggle();
	})


	$(".rotate").on("click", function () {
		console.log("toggling down class");
	    $(this).toggleClass("down");
	})
}

$(addMenuResponsivity);


var $window = $( window ); // so you have a "cached" reference 
var breakpoint = 640;

$window.resize ( function () {
	// console.log("calling resize");
		if ($window.width() > breakpoint ) {
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