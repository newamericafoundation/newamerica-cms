import $ from 'jquery'

// import getJQueryObjects from './../../utilities/get_jquery_objects.js'

// import {
//   CONTAINER_CLASS_NAME,
//   LINK_GROUP_CLASS_NAME,
//   LINK_GROUP_CONTENT_CLASS_NAME
// } from './constants.js'

var desktopHeaderBreakpoint = 945;
var expandedHeaderBreakpoint = 750;
var currHeaderBreakpoint = desktopHeaderBreakpoint;

var headerMenuExpanded = false;
var sideMenuExpanded = false;

function addMenuResponsivity() {
	$(".mobile-nav__main").on("click", function() {
		// toggle arrow for header, ensure arrow up for sidemenu
		$(".mobile-nav__toggle__main").toggleClass("down");
		$(".mobile-nav__toggle__secondary").removeClass("down");

		// toggle header menu and ensure sidemenu hidden
		$(".mobile-header-menu").toggle();
		$(".sidemenu").css("display", "none");
		sideMenuExpanded = false;

		// if expanding header, hide content and footer, else show content and footer
		if (headerMenuExpanded) {
			$(".content-container").css("display", "table-cell");
			$("footer").css("display", "block");
			headerMenuExpanded = false;
		} else {
			$(".content-container").css("display", "none");
			$("footer").css("display", "none");
			headerMenuExpanded = true;
		}
		
	})

	$(".mobile-nav__secondary").on("click", function() {
		console.log("toggling sidemenu");
		// toggle arrow for sidemenu, ensure arrow up for header
		$(".mobile-nav__toggle__secondary").toggleClass("down");
		$(".mobile-nav__toggle__main").removeClass("down");

		$(".sidemenu").toggle();
		$(".mobile-header-menu").css("display", "none");
		headerMenuExpanded = false;
		// sidemenuExpanded = !sidemenuExpanded;

		if (sideMenuExpanded) {
			$(".content-container").css("display", "table-cell");
			$("footer").css("display", "block");
			sideMenuExpanded = false;
		} else {
			$(".content-container").css("display", "none");
			$("footer").css("display", "none");
			sideMenuExpanded = true;
		}
	})

	console.log($("body").hasClass("header--expanded"));
	currHeaderBreakpoint = $("body").hasClass("header--expanded") ? expandedHeaderBreakpoint : desktopHeaderBreakpoint;

	addResizeListener();
}

$(addMenuResponsivity);

function addResizeListener() {
	var resizeMediaQuery = window.matchMedia("(min-width: " + currHeaderBreakpoint + "px)");
		resizeMediaQuery.addListener(WidthChange);
		WidthChange(resizeMediaQuery);
}

function WidthChange(mq) {

  if (mq.matches) {
    console.log("width is greater");
	$(".mobile-nav").css("display", "none");
	$(".mobile-header-menu").css("display", "none");
	$(".sidemenu").css("display", "block");
	$(".content-container").css("display", "table-cell");
	$("footer").css("display", "block");
	sideMenuExpanded = false;
	headerMenuExpanded = false;
  } else {
    console.log("width is less");
	$(".mobile-nav").css("display", "block");

	if (!sideMenuExpanded) {
		$(".sidemenu").css("display", "none");
		$(".content-container").css("display", "block");
	}
	if (!headerMenuExpanded) {
		$(".mobile-header-menu").css("display", "none");
	}
  }

}

// $window.resize ( function () {
// 	console.log($window.width());
// 	// console.log("calling resize");
// 		if ($window.width() >= currHeaderBreakpoint ) {
// 			// if (clicked == true ) {
// 				console.log("width is greater");
// 				$(".mobile-sidemenu").css("display", "none");
// 		    	$(".sidemenu").css("display", "block");
// 		    	$(".mobile-header").css("display", "none");
// 				$(".content-container").css("display", "table-cell");
// 				$("footer").css("display", "block");
// 				sideMenuExpanded = false;
// 				headerMenuExpanded = false;
			
// 	  	} else {
// 	  		console.log("width is less");
// 	  		$(".mobile-sidemenu").css("display", "block");

// 	  		if (!sideMenuExpanded) {
// 	  			$(".sidemenu").css("display", "none");
// 	  		}
// 	  		if (!headerMenuExpanded) {
// 	  			$(".mobile-header").css("display", "none");
// 	  		}
// 	  	} 
	
// });