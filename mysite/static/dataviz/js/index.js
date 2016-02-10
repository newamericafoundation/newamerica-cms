function VizController(dataFile, varJSON, divContainer) {
	console.log(varJSON);

	var data;
	var viz = {};
	var filters = [];
	var currInteraction = {
		dataFilter : null,
		timeFilter : {filterName:"birth_third_grade_rating", filterType:"continuous", filterRange: null},
		hover : null,
	}
	var currFilter = 0;
	var colorScales;

	// var dropDown = d3.select("#filter").append("select")
 //        .attr("name", "variable-list");
 var dropVal = d3.select("#filter").selectAll("option");
       console.log(dropVal);
	// d3.select(document.body)
	//     .append('div')
	//     .call(d3.slider());
	// var states = [
	// "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District Of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota","Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
	// ];

	// var svg = d3.select(".block-map").append("svg")
	// 	.attr("width", width)
	// 	.attr("height", height);
	

	d3.csv("../media/" + dataFile, function(d) {
		data = d;

		setColorScales();
		setFilterOptions();
		setTimeSlider();
		createMap();
		// var options = dropDown.selectAll("option")
	 //           .data(data)
	 //         .enter()
	 //           .append("option");

		varJSON.integratedChartOption == "display integrated chart" ? createCharts() : null;
		//data = addStateIDs(d);
		console.log(d);


	});

	// SETUP FUNCTIONS //

	function setColorScales() {
		switch(varJSON.colorScale){
			default:
				//console.log("color scale not yet supported");
				colorScales = {
					numerical: d3.scale.quantize()
						.domain([0,51])
						.range(['#005753','#3F817E', '#7FABA9', '#BFD5D4','#FFF']),
					categorical: d3.scale.ordinal()
				  		.range(['#32a1d9','#3a74bf','#7612a7','#4f38ad'])
				};
				// colorScales = d3.scale.quantize()
				// .domain([0,51])
				// .interpolate(d3.interpolateRgb)
				// 	.range(['#005753','white']);

				// var interp = d3.interpolateRgb('#005753','white');
				// var color = d3.scale.linear()
				//     .range(['#005753','white'])
				//     .interpolate(d3.interpolateRgb);
				// console.log(color(.5));
		}
	}

	// crossfilter will not allow more than 32 dimensions at a time 
	function setFilterOptions() {
		varJSON.filterVariables.forEach(function(variable, i) {
			//remove extraneous quotes
			var variable = variable.substring(1, variable.length-1);
			var varType = i > 1 ? "categorical" : "numerical";
			filters.push({filterName:variable, filterType:varType});
		});
		console.log(filters);
		currInteraction.dataFilter = filters[0];

		$("#filter").on("change", changeFilter);
		// var crossfil = crossfilter(data);
		
		// varJSON.filterVariables.forEach(function(variable, i) {
		// 	//remove extraneous quotes
		// 	var variable = variable.substring(1, variable.length-1);

		// 	filter_var[i] = {
		// 		variable_name: variable,
		// 		dimension: crossfil.dimension(function(d) { return (d[variable]);}),
		// 	}
		// });

		// var rating = cross.dimension(function(d) {return Number(d["birth_third_grade_rating"]);});
		// print_filter(filters[2].filter());
	}

	function setTimeSlider() {
		var extent = getMinMax(currInteraction.timeFilter.filterName);
		currInteraction.timeFilter.filterRange = extent;
	    $( "#slider-range" ).slider({
			range: true,
			min: extent[0],
			max: extent[1],
			values: [ extent[0], extent[1] ],
			slide: function( event, ui ) {
				currInteraction.timeFilter.filterRange = ui.values;
				updateAll();
			}
	    });
    
	}

	function createMap() {
		switch(varJSON.mapType){
			case 'heatmap':
				viz.map = Heatmap().width(1000).height(500).data(data).interaction(currInteraction).colorScale(colorScales).divContainer("#map");
				viz.map();
			default:
				console.log("map type not yet supported");
		}
	}

	function createCharts() {
		switch(varJSON.integratedChartType){
			default:
				console.log("chart type not yet supported");
		}
	}

	//UPDATE FUNCTIONS

	function updateAll() {
		viz.map.update(currInteraction);
	}

	function changeFilter() {
		var newFilter = $("#filter").val()
		console.log(newFilter);

		currInteraction.dataFilter = filters[newFilter];
		updateAll();
	}

	// function updateTime(range) {
	// 	console.log(range);
	// 	viz.map.updateTime(range);
	// }

	// function updateFilter(filter) {
	// 	console.log(range);
	// 	viz.map.update(range);
	// }


	function renderAll() {

	}


	//UTILITY FUNCTIONS

	function print_filter(filter){
		var f=eval(filter);
		if (typeof(f.length) != "undefined") {}else{}
		if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
		if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
		console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
	}

	function getMinMax(variable) {
		return d3.extent(data, function(d) { return Number(d[variable]);});
	} 
}



// function addStateIDs(d) {
// 	for (i in d) {
// 		for (j in states) {
// 			if (d[i].name.trim().toLowerCase() == states[j].toLowerCase()) {
// 				d[i].stateID = j;
// 				break;
// 			}
// 		}
// 	}
// 	return d;
// }

// function globalMouseover(stateID) {
// 	console.log("called global mouseover");
// 	//console.log(scatterplot.height());
// 	//scatterplot.hovered(stateID);
// }

	

	