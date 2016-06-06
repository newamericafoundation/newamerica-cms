import $ from 'jquery';
/*

Adds mobile menu interaction 
    - toggles display of mobile menu and hides/shows page content when menu toggle arrows are clicked
    - calls function to add resize listener to ensure that if window is resized while mobile menus are displayed,
    	page content is displayed when out of mobile mode
	- calls function to ensure that mobile menu toggle arrows rotate when menu is toggled

*/

let headerMenuExpanded = false;
let sideMenuExpanded = false;

export default function addMenuResponsivity() {
	$('.mobile-nav__main').on('click', function() {
		// toggle mobile menu arrow for main, ensure arrow up for secondary
		$('.mobile-nav__toggle__main').toggleClass('down');
		$('.mobile-nav__toggle__secondary').removeClass('down');

		// toggle header menu and ensure mobile sidemenu hidden
		$('.mobile-header').toggle();
		$('.sidemenu-container').css('display', 'none');
		sideMenuExpanded = false;

		// if expanding header, hide content and footer, else show content and footer
		if (headerMenuExpanded) {
			$('.content-container').css('display', 'table-cell');
			$('footer').css('display', 'block');
			headerMenuExpanded = false;
		} else {
			$('.content-container').css('display', 'none');
			$('footer').css('display', 'none');
			headerMenuExpanded = true;
		}

	});

	$('.mobile-nav__secondary').on('click', function() {
		// toggle mobile menu arrow for secondary, ensure arrow up for main
		$('.mobile-nav__toggle__secondary').toggleClass('down');
		$('.mobile-nav__toggle__main').removeClass('down');

		// toggle sidemenu and ensure mobile header menu hidden
		$('.mobile-sidemenu').css('display', 'block');
		$('.mobile-header').css('display', 'none');
		headerMenuExpanded = false;

		// if expanding mobile sidemenu, hide content and footer, else show content and footer
		if (sideMenuExpanded) {
			$('.sidemenu-container').css('display', 'none');
			$('.content-container').css('display', 'table-cell');
			$('footer').css('display', 'block');
			sideMenuExpanded = false;
		} else {
			$('.sidemenu-container').css('display', 'table-cell');
			$('.content-container').css('display', 'none');
			$('footer').css('display', 'none');
			sideMenuExpanded = true;
		}
	});

	addResizeListener();

	addMobileMenuArrowInteraction()
}

/*

Resize listener to ensure that if window is resized while mobile menus are displayed,
    	page content is displayed when out of mobile mode
    	- breakpoint width is based on currHeaderBreakpoint variable

*/
function addResizeListener() {
	// tracks which breakpoint to use in resize function - based on header--expanded body class
	var whichHeaderBreakpoint = $('body').hasClass('header--expanded') ? global.headerBreakpoints.expandedHeader : global.headerBreakpoints.desktopHeader;
	const resizeMediaQuery = window.matchMedia(whichHeaderBreakpoint);
		resizeMediaQuery.addListener(WidthChange);
		WidthChange(resizeMediaQuery);
}

/*

Function called by resize listener to hide/show appropriate elements

*/
function WidthChange(mq) {
	if (mq.matches) {
		// screen width is greater than breakpoint -> hide mobile elements, make sure page content elements are displayed, 
		//		toggle menu arrows back up
		$('.mobile-nav').css('display', 'none');
		$('.mobile-header').css('display', 'none');
		$('.mobile-sidemenu').css('display', 'none');
		$('.sidemenu').css('display', 'block');
		$('.sidemenu-container').css('display', 'table-cell');
		$('.content-container').css('display', 'table-cell');
		$('footer').css('display', 'block');
		$('.mobile-nav__toggle__main').removeClass('down');
		$('.mobile-nav__toggle__secondary').removeClass('down');
		sideMenuExpanded = false;
		headerMenuExpanded = false;
	} else {
		// screen width is less than breakpoint -> display mobile elements
		$('.mobile-nav').css('display', 'block');
		$('.sidemenu').css('display', 'none');

		if (!sideMenuExpanded) {
			$('.sidemenu-container').css('display', 'none');
			$('.content-container').css('display', 'block');
		}
		if (!headerMenuExpanded) {
			$('.mobile-header').css('display', 'none');
		}
	}
}

/*

Rotates arrows when mobile menu item is clicked, changes color for secondary menu arrows on hover

*/
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
