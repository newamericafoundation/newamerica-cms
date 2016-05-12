import $ from 'jquery';

/*

Pre-populates subscribe form email field from query parameter in URL string. 

*/
export default function populateEmailField() {
	var email = getParameterByName('email');
	$("#fieldEmail").val(email);
}

/*

Parses URL, returning value for specified field, returns null if not found
	parameters: name - name of variable in query string
				url - url string

*/
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}
