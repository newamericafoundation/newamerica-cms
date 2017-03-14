import $ from 'jquery';

import { axisBottom } from 'd3-axis';
import { scaleLinear, scalePoint, scaleQuantize } from 'd3-scale';
import { extent, ascending } from 'd3-array';
import { select, selectAll } from 'd3-selection';
import { nest } from 'd3-collection';
import { timeFormat } from 'd3-time-format';
import { timeDay, timeMonth, timeYear } from 'd3-time';

const dotRadius = 8,
	dotOffset = 5,
	margin = { left: 15, right: 15, top: 20, bottom: 50},
	strokeColor = "#c0c1c3",
	strokeSelectedColor = "#2c2f35",
	fillColor = "#fff",
	fillSelectedColor = "#2c2f35";

class Timeline {
	constructor() {
		this.svg = select(".timeline__nav")
				.append("svg")
				.attr("class", "timeline__nav__container")
				.attr("width", "100%"); 

		this.g = this.svg.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		this.xScale = scaleQuantize()
			.domain(extent(eventList, (d) => { return new Date(d.start_date) }));
		this.yScale = scaleLinear();

		this.xAxis = this.svg.append("g")
			.attr("class", "timeline__nav__axis")
			.attr("class", "axis axis-x");

		this.hoverInfo = this.svg.append("g")
			.attr("class", "timeline__nav__hover-info")
			.classed("hidden", true);
		this.hoverInfoText = this.hoverInfo.append("text");
		
		this.setTimeFormat();
		this.currSelected = 0;
		select("#event-0").classed("visible", true);

		this.render();

		window.addEventListener('resize', this.resize.bind(this));

	}

	render() {
		this.setWidth();
		this.setXRange();
		this.setDataNest();
		this.setHeight();
		this.setYScale();
		this.setCircles();
	}

	setWidth() {
		this.w = $(".timeline__nav").width() - margin.left - margin.right;

		this.g
			.attr("width", this.h);
	}

	setHeight() {
		this.h = this.numRows * (dotRadius*2 + dotOffset);
		this.svg
			.attr("height", this.h + margin.top + margin.bottom);

		this.g
			.attr("height", this.h);

		this.xAxis
			.attr("transform", "translate(" + margin.left + "," + (this.h + margin.top + dotRadius + dotOffset) + ")")
			.call(axisBottom(this.xScale).tickPadding(10).tickSizeOuter(0).tickFormat(this.timeFormat));
	}

	setXRange() {
		const numCols = Math.floor(this.w/(2*dotRadius + dotOffset));
		let colBins = [];

		let linearXScale = scaleLinear()
			.domain([0, numCols])
			.range([0, this.w]);

		for (let i = 0; i < numCols; i++) {
			colBins[i] = linearXScale(i);
		}

		this.xScale.range(colBins);
	}

	setYScale() {
		console.log(this.numRows, this.h)
		this.yScale
			.domain([0, this.numRows])
			.range([this.h, 0]);
	}

	setDataNest() {
		let maxLength = 0;
		this.dataNest = nest()
			.key((d) => { return this.xScale(new Date(d.start_date)); })
			.sortValues(ascending)
			.rollup((d) => { maxLength = Math.max(maxLength, d.length); return d; })
			.entries(eventList);

		this.numRows = maxLength;
		console.log(this.dataNest);
	}

	setCircles() {
		for (let column of this.dataNest) {
			let i = 0;
			for (let value of column.value) {
				this.g.append("rect")
				    .attr("x", Number(column.key) - dotRadius)
				    .attr("y", () => { console.log(i, this.yScale(i)); return this.yScale(i) - dotRadius; })
				    .attr("height", dotRadius*2)
				    .attr("width", value.end_date ? this.xScale(new Date(value.end_date)) - Number(column.key) - dotOffset : dotRadius*2)
				    .attr("rx", dotRadius)
				    .attr("ry", dotRadius)
				    .attr("class", "timeline__nav__dot")
				    .classed("selected", value.id == this.currSelected)
				    .on("mouseover", (d, index, paths) => { return this.mouseover(value, paths[index]); })
				    .on("mouseout", (d, index, paths) => { return this.mouseout(paths[index]); })
				    .on("click", (d, index, paths) => { return this.clicked(value, paths[index]); });
				i++;
			}
		}
	}

	setTimeFormat() {
		const [minTime, maxTime] = this.xScale.domain();

		if (timeMonth.count(minTime, maxTime) < 6) {
			this.timeFormat = timeFormat("%B %d, %Y");
		} else if (timeMonth.count(maxTime - minTime) < 18) {
			this.timeFormat = timeFormat("%B %Y");
		} else {
			this.timeFormat = timeFormat("%Y");
		}
	}

	resize() {
		console.log("resizing");

		this.g.selectAll("rect").remove();

		this.render()
	}

	mouseover(datum, path) {
		let elem = select(path);
		elem.classed("hovered", true);

		this.hoverInfo
			.classed("hidden", false)
			.attr("transform", "translate(" + elem.attr("x") + "," + 10 + ")");

		this.hoverInfoText.text(datum.title);
	}

	mouseout(path) {
		select(path).classed("hovered", false);

		this.hoverInfo.classed("hidden", true);
	}

	clicked(datum, path) {
		const { id } = datum;
		select("#event-" + this.currSelected).classed("visible", false);
		select(".timeline__nav__dot.selected").classed("selected", false);
		this.currSelected = id;
		select("#event-" + id).classed("visible", true);
		select(path).classed("selected", true);
	}
}

export default function() {
	console.log("loaded script!");
	console.log(eventList);
	const timeline = new Timeline();

	
}