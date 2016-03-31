import $ from 'jquery'

// removes dropcap if body height is less than cutoff
function checkBodyHeight() {
	var dropcapCutoff = 70;
	var $post_body = $(".post-body");
	var bodyHeight = $post_body.height();

	if (bodyHeight < dropcapCutoff) {
		$post_body.removeClass("with-dropcap");
	}
}

$(checkBodyHeight);