import $ from 'jquery'
/*
	in-depth/index.js - adds in-depth section header interaction,
		- implements slick carousel - documentation: http://kenwheeler.github.io/slick/

*/

export default function() {
	if( $('body').hasClass('template-indepthsection') ){
		addSectionHeaderInteraction();
		inDepthPanelScroll();
	}
}

/*

	Implements slick carousel for in-depth section header, adds event listener and calls initially
		helper function to toggle carousel arrows on scroll

*/
