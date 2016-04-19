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

function styleFirstLine() {
	var $first_paragraph = $(".with-dropcap .block-paragraph:first-child p:first-child");

	var sentences = $first_paragraph.text().split('.');
	
	sentences[0] = "<span class=post-body__first-sentence>" + sentences[0] + ".</span>";
	console.log(sentences);

	$first_paragraph.html(sentences.join('.'))
}

$(checkBodyHeight);
$(styleFirstLine);