function Heatmap()  {
	//default values - overidden if user passes in arguments
	var width = 1000;
	var height = 500;
	var divContainer = "body";
	var data, colorScale;
	var currInteraction;
	var geography;
	var paths;
	//pass in from index.js
	var numBins = 5;

	var path = d3.geo.path();
	var tooltip = d3.select(divContainer)
		    .append("div")
		    .classed("tooltip", true)
		    .style("visibility", "hidden")
		    .text("");

	function my() {
		// var filter_default = filters[curr_filter].variable_name;
		var filterDefault = "birth_third_grade_rating";


		var svg = d3.select(divContainer).append("svg")
			.attr("width", width)
			.attr("height", height)

		processData();

		function processData() {
			console.log(data);
			// var data_subset = filters[curr_filter].dimension.filter([0,35]).top(Infinity);
			// console.log(data_subset.valueOf());
			d3.json("../static/dataviz/geography/us-states.json", function(json) {
				geography = json;
				
				for (i in data) {
					var state = data[i];
					for (j in geography.features) {
						if (state.name.trim().toLowerCase() == geography.features[j].properties.name.toLowerCase()) {
							// change to only transfer fields needed for filtering, sidebar, etc
							Object.keys(state).forEach(function(field) {
								// console.log(state[field]);
								geography.features[j].properties[field] = state[field];
							});	
							// geography.features[j].properties[filterDefault] = state[filterDefault];
							// geography.features[j].properties["educators_ranking"] = state["educators_ranking"];
							// geography.features[j].properties.stateID = state.stateID;
							break;
						}
					}
				}
				render();
			});
		}
		
		function render() {
			paths = svg.selectAll("path")
				.data(geography.features)
				.enter()
				.append("path")
				.attr("d", path)
				.style(function(d) { return findFill(d);})
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
			var dataProps = d3.select(this)[0][0].__data__.properties;
			tooltip.style("top", (event.pageY-10)+"px").style("left",(event.pageX+10)+"px")
				.text(function() { return dataProps.name + "\n" + dataProps[currInteraction.dataFilter.filterName] ;});
		}

		function mouseout() {
			d3.select(this)
				.attr("fill", function(d) { return findFill(d);});
			tooltip.style("visibility", "hidden");
		}
	}

	my.update = function(interaction) {
		currInteraction = interaction;

		paths.style(function(d) {return findFill(d);});

		return my;
	}

	function findFill(d) {
		var dataVal = d.properties[currInteraction.dataFilter.filterName];
		var timeVal = d.properties[currInteraction.timeFilter.filterName];
		var filterType = currInteraction.dataFilter.filterType;

		if (isWithinTimeRange(timeVal) && isToggled(dataVal)) {
			var color = String(colorScale[filterType](dataVal));
			return {fill: color, stroke: 'grey'};
		} else {
			return {fill: 'none', stroke: 'white'};
		}
	}

	function isWithinTimeRange(timeVal) {
		if (timeVal >= currInteraction.timeFilter.filterRange[0] && timeVal <= currInteraction.timeFilter.filterRange[1]) {
			return true;
		} else {
			return false;
		}
	}

	function isToggled(dataVal) {
		if (currInteraction.dataFilter.filterType == "categorical") {
			console.log(currInteraction.dataFilter.filterValues[dataVal]);
			return currInteraction.dataFilter.filterValues[dataVal];
		} else {
			console.log(dataVal);
			console.log(currInteraction.dataFilter.filterValues[whichBin(dataVal)]);
			return currInteraction.dataFilter.filterValues[whichBin(dataVal)];
		}
		
		
	}

	function whichBin(dataVal) {
		console.log(dataVal);
		var interval = currInteraction.dataFilter.filterInterval;
		var bin = Math.floor(dataVal/interval);
		console.log(bin);
		return bin >= numBins ? (numBins - 1): bin;
	}

	//Getter and Setter functions

	my.width = function(value) {
		if (!arguments.length) return width;
		width = value;
		return my;
	};

	my.height = function(value) {
		// console.log("here");
		if (!arguments.length) return height;
		height = value;
		return my;
	};

	my.data = function(value) {
		if (!arguments.length) return data;
		data = value;
		return my;
	};

	my.interaction = function(value) {
		if (!arguments.length) return currInteraction;
		currInteraction = value;
		return my;
	};

	my.colorScale = function(value) {
		if (!arguments.length) return colorScale;
		colorScale = value;
		return my;
	};

	my.divContainer = function(value) {
		if (!arguments.length) return divContainer;
		divContainer = value;
		return my;
	};

	return my;
}