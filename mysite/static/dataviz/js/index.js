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
	var numBins = 5;



	data = d3.csv.parse(dataFile);
	console.log(data);
	setColorScales();
	setFilterOptions();
	setValueButtons();
	setTimeSlider();

	console.log(currInteraction);

	createMap();

	varJSON.integratedChartOption == "display integrated chart" ? createCharts() : null;


	// var dropDown = d3.select("#filter").append("select")
 //        .attr("name", "variable-list");
 // var dropVal = d3.select("#filter").selectAll("option");
       // console.log(dropVal);
	// d3.select(document.body)
	//     .append('div')
	//     .call(d3.slider());
	// var states = [
	// "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District Of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota","Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
	// ];

	// var svg = d3.select(".block-map").append("svg")
	// 	.attr("width", width)
	// 	.attr("height", height);
	
		// d3.csv("../media/documents/crawling-to-walking1_1.csv", function(d) {
		// d3.csv("../media/" + dataFile, function(d) {
		// console.log(dataFile);
		

		// , function(d) {
		// 	console.log(d);
		// 	console.log('running again');
			// data = d;
			// console.log(data);
			// setColorScales();
			// setFilterOptions();
			// getValueButtons();
			// setTimeSlider();


			// console.log(currInteraction);
			// createMap();
			// var options = dropDown.selectAll("option")
		 //           .data(data)
		 //         .enter()
		 //           .append("option");

			// varJSON.integratedChartOption == "display integrated chart" ? createCharts() : null;
			// //data = addStateIDs(d);
			// // console.log(d);

			// var checkboxes = $("fieldset");
			// console.log(checkboxes);
		// });
		// console.log(data);
	
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
		var dropdown = $('#filter');

		varJSON.filterVariables.forEach(function(variable, i) {
			//remove extraneous quotes
			var filtName = variable.substring(1, variable.length-1);
			var filtType = i > 1 ? "categorical" : "numerical";
			if (filtType == "categorical") {
				var filtValues = setFilterValues(filtName);
				var filtRange = null;
				var filtInterval = null;
			} else {
				var filtValues = setFilterBins(filtName);
				var filtInterval = setFilterInterval(filtName)
				//range only needed for time filters - might be able to get rid of
				var filtRange = setFilterRange(filtName);
			}

			filters.push({filterName:filtName, filterType:filtType, filterValues:filtValues, filterRange:filtRange, filterInterval:filtInterval});
			$('<option />', {value: i, text: filtName}).appendTo(dropdown);
		});
		console.log(filters);
		currInteraction.dataFilter = filters[0];
		//set to whichever user imputs as time filter var
		currInteraction.timeFilter = filters[0];

		dropdown.on("change", changeFilter);
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
		// var extent = getMinMax(currInteraction.timeFilter.filterName);
		var currRange = currInteraction.timeFilter.filterRange;
	    $( "#slider-range" ).slider({
			range: true,
			min: currRange[0],
			max: currRange[1],
			values: [ currRange[0], currRange[1] ],
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
		setValueButtons();
		updateAll();
	}

	

	function setFilterValues(filtName) {
		var vals = {};
		var uniqueVals = d3.map(data, function(d){return d[filtName]}).keys();

		for (i in uniqueVals) {
			var currVal = uniqueVals[i];
			vals[currVal] = true;
		}
		return vals;
	}

	// function getNumFilterValues(filtName, range) {
	// 	var numBins = 5;
	// 	var interval = (range[1]-range[0])/numBins;
	// 	console.log(interval);
	// 	var valBins = {};

	// 	for (var i = 0; i < numBins; i++) {
	// 		console.log(i);
	// 		var currBinStart = i*interval;
	// 		var currBinEnd = i*interval
	// 		valBins[currBin] = true;
	// 	}

	// 	console.log(valBins);

	// 	return range;
	// }

	function setFilterBins(filtName) {
		var bins = {};
		for (var i = 0; i < numBins; i++) {
			bins[i] = true;
		}
		return bins;
	}

	function setFilterInterval(filtName) {
		var range = setFilterRange(filtName);
		return (range[1]-range[0])/numBins;
	}

	function setFilterRange(filtName) {
		return d3.extent(data, function(d) { return Number(d[filtName]);});
	}

	function setValueButtons() {
		var currFilter = currInteraction.dataFilter;
		var interval = currFilter.filterInterval;
		var buttonContainer = $('#viz-block__filter-buttons');
		buttonContainer.empty();
		
		var i = 0;
		for (val in currFilter.filterValues) {
			var label = interval ? binLabel(i) : val;
			$('<input id=filter-val' + i + ' type="checkbox" checked="checked" value="' + val + '"><label for=filter-val' + i + '">' + label + '</label>')	
				.appendTo(buttonContainer)
				.on("click", function(e) { buttonToggled(this.value);});
			i++;
		}
		// 			// .on("click", function(e) {
		// 	var i = 0;
		// 	for (val in currFilter.filterValues) {
		// 		if ()
		// 		$('<input id=filter-val' + i + ' type="checkbox" checked="checked" value="' + val + '"><label for=filter-val' + i + '">' + val + '</label>')	
		// 			.appendTo(buttonContainer)
		// 			// .on("click", function(e) {
		// 			// 	console.log(e);
		// 			// 	var val = e.target.value;
		// 			// 	console.log(val);
		// 			// 	currFilter.filterValues[val].toggled = !currFilter.filterValues[val].toggled;
		// 			// 	updateAll();
		// 			// });
          		
		// 		// $('<li><a href="#" class="small button">' + val + '</a></li>').appendTo(buttonContainer);
		// 	}

		// } else {
		// 	console.log("needs to get range for numerical values")
		// }

	}

	function binLabel(binNum) {
		var interval = currInteraction.dataFilter.filterInterval;
		if (binNum >= numBins -1) {
			return binNum*interval + "+";
		} else {
			return binNum*interval+1 + " to " + ((binNum+1)*interval);
		}
	}

	function buttonToggled(value) {
		currInteraction.dataFilter.filterValues[value] = !currInteraction.dataFilter.filterValues[value];
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


	//UTILITY FUNCTIONS

	

	
}

// function print_filter(filter){
// 		var f=eval(filter);
// 		if (typeof(f.length) != "undefined") {}else{}
// 		if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
// 		if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
// 		console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
// 	}

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

	

	