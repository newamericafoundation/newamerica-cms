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
	margin = { left: dotRadius, right: dotRadius, top: dotRadius, bottom: 50};

class Timeline {
	constructor() {
		this.svg = select(".timeline__nav")
				.append("svg")
				.attr("width", "100%"); 

		this.g = this.svg.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		this.xScale = scaleQuantize()
			.domain(extent(eventList, (d) => { return new Date(d.start_date) }));
		this.yScale = scaleLinear();

		this.xAxis = this.svg.append("g")
			.attr("class", "axis axis-x");
		
		this.setTimeFormat();

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
				this.g.append("circle")
					.attr("r", dotRadius)
				    .attr("cx", Number(column.key))
				    .attr("cy", () => { console.log(i, this.yScale(i)); return this.yScale(i); })
				    .attr("fill", "#fff")
				    .attr("stroke", "grey");
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

		this.g.selectAll("circle").remove();

		this.render()
	}
}

export default function() {
	console.log("loaded script!");
	console.log(eventList);
	const timeline = new Timeline();

	
}