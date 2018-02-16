
import bowser from 'bowser';
import domtoimage from 'dom-to-image';

export default function dataVizEvents() {
	let viz = document.querySelectorAll('.dataviz');
	if(!viz) return;

	for(let v of viz){

		//v.onclick = function(e) { e.stopPropagation(); }

		var chartArea = v.querySelector('.dataviz__chart-area'),
			downloadLink = v.querySelector('.dataviz__download-link'),
			embedLink = v.querySelector('.dataviz__embed-link'),
			shareLink = v.querySelector('.dataviz__share-link');

		if(downloadlink)
			downloadLink.onclick = () => { handleDownloadClickEvent(chartArea) };

		if(embedLink)
			embedLink.onclick = shareLink.onclick = function(){
				this.style.display == 'none' ? this.style.display = '' : this.style.display = 'none';
			}

		document.body.onclick = function(e){
			embedPopup.style.display = 'none';
			sharePopup.style.display = 'none';
		}
		// hides download links on Internet Explorer
		hideDownloadLink(downloadLink);

	}
}

function handleDownloadClickEvent(chartArea) {
	chartArea.style.backgroundColor = 'white';
	domtoimage.toPng(chartArea)
	    .then((dataUrl) => {
	    	var id = $(chartArea).attr("id");
			var link = document.createElement("a");
		    link.download = id + '.png';
		    link.href = dataUrl;
		    link.click();
		    link.remove();
				chartArea.style.backgroundColor = 'none';
	    })
	    .catch(function (error) {
	        console.error('oops, something went wrong!', error);
	    });
}

// hides download links on Internet Explorer and shows alternative download data message
function hideDownloadLink(downloadLink) {
	if (bowser.msie) {
		downloadLink.style.display = 'none'
		document.querySlector('.in-depth__footer__download-data-message').style.display = '';
	} else if (bowser.safari) {
		document.querySlector('.in-depth__footer__download-data-message').style.display = '';
	}
}
