import $ from 'jquery'

import getJQueryObjects from './../../utilities/get_jquery_objects.js'

function addSidemenuInteractivity() {
	$(".mobile-sidemenu__toggle").on("click", function() {
		console.log("clicked!");
		$(".sidemenu").toggle();
		$(".content-container").toggle();
		$("footer").toggle();
	})


}

$(addSidemenuInteractivity)
