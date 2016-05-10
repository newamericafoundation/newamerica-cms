import $ from 'jquery';

const OTIurl = 'oti';

export default function checkOTI() {
	const url = window.location.href;
	const urlPieces = url.split('/');
	for (let i in urlPieces) {
		if (urlPieces[i].toLowerCase() === OTIurl) {
			$('.wrapper').addClass('oti');
		}
	}
}
