function VizController(data_file, varJSON, div_container) {
	console.log(varJSON);

	var data;
	var viz = {};
	var filt_var = [];
	var col_scale;

	// d3.select(document.body)
	//     .append('div')
	//     .call(d3.slider());
	// var states = [
	// "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District Of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota","Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
	// ];

	// var svg = d3.select(".block-map").append("svg")
	// 	.attr("width", width)
	// 	.attr("height", height);
	

	d3.csv("../media/" + data_file, function(d) {
		data = d;

		setColorScale();
		setFilterVariables();
		createMap();
		varJSON.integratedChartOption == "display integrated chart" ? createCharts() : null;
		//data = addStateIDs(d);
		console.log(d);
		d3.select("div#slider3")
            .call(d3.slider().axis(true).min(0).max(100).value(75));

	});

	function setColorScale() {
		switch(varJSON.colorScale){
			default:
				//console.log("color scale not yet supported");
				col_scale = d3.scale.linear()
					.domain([0,51])
					.range(['#005753','white']);
		}
	}

	// crossfilter will not allow more than 32 dimensions at a time 
	function setFilterVariables() {
		var crossfil = crossfilter(data);
		
		varJSON.filterVariables.forEach(function(variable, i) {
			filt_var[i] = {
				variable_name: variable,
				dimension: crossfil.dimension(function(d) {return (d[variable]);})
			}
		});

		// var rating = cross.dimension(function(d) {return Number(d["birth_third_grade_rating"]);});
		// print_filter(filters[2].filter());
	}

	function createMap() {
		switch(varJSON.mapType){
			case 'heatmap':
				viz.map = Heatmap().width(1000).height(500).data(data).filters(filt_var).color_scale(col_scale).div_container("#map");
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

	// function print_filter(filter){
	// 	var f=eval(filter);
	// 	if (typeof(f.length) != "undefined") {}else{}
	// 	if (typeof(f.top) != "undefined") {f=f.top(Infinity);}else{}
	// 	if (typeof(f.dimension) != "undefined") {f=f.dimension(function(d) { return "";}).top(Infinity);}else{}
	// 	console.log(filter+"("+f.length+") = "+JSON.stringify(f).replace("[","[\n\t").replace(/}\,/g,"},\n\t").replace("]","\n]"));
	// } 
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

	

	