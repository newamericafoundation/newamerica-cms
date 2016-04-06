import $ from 'jquery'

function addSubscribeInteraction() {
	$('.subscribe-form').submit(function() {
		console.log("submitted");
	});
}

$( document ).ready( function() {
	$(addSubscribeInteraction);
});