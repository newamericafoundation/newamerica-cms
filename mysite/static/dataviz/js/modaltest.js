	// console.log("getting from file");
// $( document ).append(<div id="data-visualization-customizer-app"></div>);
$( document ).ready( function() {
	$('.action-add-block-map').on('click', function() { console.log("clicked!"); startAfterInterval(250);});

	function startAfterInterval(intervalInMs) {
			setTimeout(start, intervalInMs);
	}

	function start() {
		var before_val = $('[id$=-value-data_file]').val();

		window.setInterval(function() {
			var after_val = $('[id$=-value-data_file]').val();

			if(before_val != after_val) {
				console.log("uploaded file changed");
				before_val = after_val;
				
				var response1 = $.get( "/api/v1/documents/" + after_val, function(data) {
					// console.log(url);
					var url = data.meta.download_url;

					//should replace everythign before /documents with regular expressions instead
					var doc = url.replace("http://localhost", '');
					
					var response2 = $.get(doc, function(f) {
						// console.log(f);
						window.dataVisualizationCustomizer.addCustomizer({
						  fileContent: f,
						  // fileInputSelector: '[id$=-value-data_file]',
						  optionsInputSelector: '[id$=-value-variable_option]',
						  appContainerSelector: '#data-visualization-customizer-app'
						});

					});
					// console.log(response1);
					// console.log(response2);
				});
			} 
		}, 300);
	}	
});