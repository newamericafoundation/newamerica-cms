import $ from 'jquery';

/*

Pre-populates content control filters based on url query parameters

*/
function prepopulateFormFields() {
	var queryParams = getQueryParams(document.location.search);
	$(".content-grid__controls__program-filter").val(queryParams.program_id);
	$("#content-grid__controls__date-filter").val(queryParams.date);
}

/*

Given a url query string as input, outputs an array of the query parameters

*/
function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

/*

Enables submit button when content control filter is changed

*/
function addContentControlsInteraction() {
    $(".content-grid__controls__program-filter").on("change", function() {
        $("#content-grid__controls__submit").prop('disabled', false);
    });
}

export default function() {
	prepopulateFormFields();
    addContentControlsInteraction();
}
