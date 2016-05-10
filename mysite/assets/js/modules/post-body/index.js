import $ from 'jquery';

// removes dropcap if first paragraph character count is less than cutoff
export default function checkDropcap() {
	var dropcapCutoff = 300;
	var $first_paragraph = $(".with-dropcap > .block-paragraph:first-child p:first-child");
	var paragraphLength = $first_paragraph.text().length;

	if (paragraphLength < dropcapCutoff) {
		$(".with-dropcap").removeClass("with-dropcap");
	}
}
