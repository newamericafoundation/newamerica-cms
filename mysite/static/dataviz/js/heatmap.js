function Heatmap()  {
	//default values - overidden if user passes in arguments
	var width = 1000;
	var height = 500;
	var div_container = "body";
	var data, filters, color_scale;
	var geography;

	var path = d3.geo.path();
	var tooltip = d3.select(div_container)
		    .append("div")
		    .classed("tooltip", true)
		    .style("visibility", "hidden")
		    .text("");

	function my() {
		var curr_filter = 0;
		// var filter_default = filters[curr_filter].variable_name;
		var filter_default = "birth_third_grade_rating";


		var svg = d3.select(div_container).append("svg")
			.attr("width", width)
			.attr("height", height)
			
			// 	.on("slide", function(evt, value) {
			//   d3.select('#slider3textmin').text(value[ 0 ]);
			//   d3.select('#slider3textmax').text(value[ 1 ]);
			// }));

		// svg.append("div")
		// 	.attr("width", width)
		// 	.attr("height", height)
  //           .call(d3.slider().axis(true).min(0).max(10));

		processData();

		function processData() {
			console.log(data);
			d3.json("../static/dataviz/geography/us-states.json", function(json) {
				geography = json;
				
				for (i in data) {
					var state = data[i];
					for (j in geography.features) {
						// console.log(geography.features[j].properties[birth_third_grade_rating]);
						console.log(state[filter_default]);
						if (state.name.trim().toLowerCase() == geography.features[j].properties.name.toLowerCase()) {
							geography.features[j].properties[filter_default] = state[filter_default];
							geography.features[j].properties.stateID = state.stateID;
							break;
						}
					}
				}
				render();
			});
		}
		
		function render() {
			svg.selectAll("path")
				.data(geography.features)
				.enter()
				.append("path")
				.attr("d", path)
				.attr("fill", function(d) {
				    var value = d.properties[filter_default];
				    // console.log(value);
				    //returns grey if value is undefined
				    return value ? color_scale(value) : "#ccc";
				})
				.on("mouseover", mouseover)
				.on("mousemove", mousemove)
				.on("mouseout", mouseout);
		}
		
		function mouseover() {
			var elem = d3.select(this)
				.attr("fill", "orange");
			tooltip.style("visibility", "visible");
			// globalMouseover(elem[0][0].__data__.properties.stateID);
		}

		function mousemove() {
			var dataProps= d3.select(this)[0][0].__data__.properties;
			tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px")
				.text(function() { return dataProps.name + "\n" + dataProps[filter_default] ;});
		}

		function mouseout() {
			d3.select(this)
				.attr("fill", function(d) {
					var value = d.properties[filter_default];
	                    //returns white if value is undefined
	                return value ? color_scale(value) : "#ccc";
				});
			tooltip.style("visibility", "hidden");
		}
	}

	//Getter and Setter functions

	my.width = function(value) {
		if (!arguments.length) return width;
		width = value;
		return my;
	};

	my.height = function(value) {
		console.log("here");
		if (!arguments.length) return height;
		height = value;
		return my;
	};

	my.data = function(value) {
		if (!arguments.length) return data;
		data = value;
		return my;
	};

	my.filters = function(value) {
		if (!arguments.length) return filters;
		filters = value;
		return my;
	};

	my.color_scale = function(value) {
		if (!arguments.length) return color_scale;
		color_scale = value;
		return my;
	};

	my.div_container = function(value) {
		if (!arguments.length) return div_container;
		div_container = value;
		return my;
	};

	return my;
}