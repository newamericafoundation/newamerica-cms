	// console.log("getting from file");
$( document ).ready( function() {
		$('.action-add-block-map').on('click', function() { console.log("clicked!"); startAfterInterval(250);});

		function startAfterInterval(intervalInMs) {
				setTimeout(start, intervalInMs);
		}

		function start() {
			var before_val = $('[id$=-value-data_file]').val();

			$(document).on('mousemove', function() {
				var after_val = $('[id$=-value-data_file]').val();
				if(before_val != after_val) {
					console.log("uploaded file changed")
					before_val = after_val;
					alert("this would be a modal with variable customization");
					window.dataVisualizationCustomizer.addCustomizerOnUpload({
						fileInputSelector: '[id$=-value-data_file]',
						optionsInputSelector: '[id$=-value-variable_option]',
						appContainerSelector: '#data-visualization-customizer-app'
					});
				} 
			});
		}	
});