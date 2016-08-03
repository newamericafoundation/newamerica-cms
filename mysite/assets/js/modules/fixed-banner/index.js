import $ from 'jquery'
/*

Adds click interaction to fixed banner close button

*/

export default function addFixedBannerCloseInteraction() {
	$(".fixed-banner__close").click(function() {
		$(".fixed-banner").hide();
		$(".footer").css("margin-bottom", "0px");
	})
}