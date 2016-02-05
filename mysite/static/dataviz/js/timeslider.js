$(function() {
	    $( "#slider-range" ).slider({
	      range: true,
	      min: 0,
	      max: 50,
	      values: [ 0, 25 ],
	      slide: function( event, ui ) {
	        console.log(ui.value);
	      }
	    });
	    
	  });