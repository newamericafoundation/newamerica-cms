import $ from 'jquery';

import { axisBottom } from 'd3-axis';
import { scaleLinear, scalePoint, scaleQuantize } from 'd3-scale';
import { extent, ascending, min, max } from 'd3-array';
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

		let minDate = min(eventList, (d) => { return new Date(d.start_date); });
		let maxDate = max(eventList, (d) => { return d.end_date ? new Date(d.end_date) : new Date(d.start_date) });

		console.log(minDate, maxDate)
		this.xScale = scaleLinear()
			.domain([minDate, maxDate]);

		this.yScale = scaleLinear();

		this.dayMonthAxis = this.svg.append("g")
			.attr("class", "timeline__nav__axis axis axis-x day-month-axis");

		this.yearAxis = this.svg.append("g")
			.attr("class", "timeline__nav__axis axis axis-x year-axis");

		this.hoverInfo = this.svg.append("g")
			.attr("class", "timeline__nav__hover-info")
			.classed("hidden", true);
		this.hoverInfoText = this.hoverInfo.append("text");

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

		this.setXAxis();

		
	}

	setXRange() {

		this.xScale.range([0, this.w]).nice();
	}

	setYScale() {
		this.yScale
			.domain([0, this.numRows])
			.range([this.h, 0]);
	}

	setDataNest() {
		let startXPos, endXPos, yIndex;
		this.rows = [];
		this.rows[0] = [];

		eventList.map((d) => {
			startXPos = this.xScale(new Date(d.start_date));
			endXPos = d.end_date ? this.xScale(new Date(d.end_date)) : startXPos;

			d.yIndex = this.calcYIndex(startXPos - dotRadius, endXPos + dotRadius);
			d.startXPos = startXPos;
			d.endXPos = endXPos;
			console.log(this.rows);
			console.log(d.yIndex);
		})

		this.numRows = 5;

		
	}

	calcYIndex(startXPos, endXPos) {	
		let i = 0;

		for (let row of this.rows) {
			let foundOverlap = false;
			// loop through all intervals stored within row
			for (let rowInterval of row) {
				// check if start or end position overlaps with interval
				if ((startXPos >= rowInterval.start && startXPos <= rowInterval.end) || 
					(endXPos >= rowInterval.start && endXPos <= rowInterval.end)) {
					// if overlap, breaks loop, moves to next row
					foundOverlap = true;
					break;
				}
			}
			// no overlap found, adding to current row
			if (!foundOverlap) {
				row.push({start:startXPos, end:endXPos});
				return i;
			}
			i++;
		}
		// could not place in current rows, adding new row
		this.rows.push([{start:startXPos, end:endXPos}]);
		return i;
	}

	setCircles() {
		this.g.selectAll("rect")
			.data(eventList)
			.enter().append("rect")
		    .attr("x", (d) => { return d.startXPos - dotOffset; })
		    .attr("y", (d) => { return this.yScale(d.yIndex) - dotOffset; })
		    .attr("height", dotRadius*2)
		    .attr("width", (d) => { return d.endXPos && (d.endXPos != d.startXPos) ? d.endXPos - d.startXPos + dotRadius*2 : dotRadius*2; })
		    .attr("rx", dotRadius)
		    .attr("ry", dotRadius)
		    .attr("class", "timeline__nav__dot")
		    .classed("selected", (d) => { return d.id == this.currSelected })
		    .on("mouseover", (d, index, paths) => { return this.mouseover(d, paths[index]); })
		    .on("mouseout", (d, index, paths) => { return this.mouseout(paths[index]); })
		    .on("click", (d, index, paths) => { return this.clicked(d, paths[index]); });
	}

	setXAxis() {
		const [minTime, maxTime] = this.xScale.domain();
		let numDays = timeDay.count(minTime, maxTime);
		let numYears = timeYear.count(minTime, maxTime);

		let tickFormat;
		let numTicks = Math.floor(this.w/100);
		let monthVals = timeMonth.range(minTime, maxTime, 3)
		let yearVals = timeYear.range(minTime, maxTime);
		console.log(yearVals);
		let dayMonthAxis = axisBottom(this.xScale).tickPadding(10).tickSizeOuter(0);
		let yearAxis = axisBottom(this.xScale).tickPadding(0).tickSizeOuter(0).tickSizeInner(0).tickValues(yearVals).tickFormat(timeFormat("%Y"));
	
		console.log(numDays, numYears);
		
		console.log(numTicks);

		if (numDays/numTicks < 30) {
			dayMonthAxis.tickFormat(timeFormat("%B %d"));
		} else if (numDays/numTicks < 270) {
			dayMonthAxis.tickFormat(timeFormat("%B")).tickValues(monthVals);
		} else {
			dayMonthAxis.tickFormat(timeFormat(""));
		}
		
		if (dayMonthAxis) {
			this.dayMonthAxis
				.attr("transform", "translate(" + margin.left + "," + (this.h + margin.top + dotRadius + dotOffset) + ")")
				.call(dayMonthAxis)
			// .selectAll('text') // `text` has already been created
			// .attr("fill", (d) => { console.log(tickFormat(d)); return "blue";})
		}

		this.yearAxis
			.attr("transform", "translate(" + margin.left + "," + (this.h + margin.top + dotRadius + dotOffset + 30) + ")")
			.call(yearAxis);

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