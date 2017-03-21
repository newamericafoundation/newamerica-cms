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
	constructor(settingsObject, navContainerId, contentContainerId) {
		console.log(settingsObject);
		this.eventList = settingsObject.event_list;
		this.eraList = settingsObject.era_list;

		console.log(this.eventList, this.eraList);
		this.navContainer = select(navContainerId);
		this.contentContainer = select(contentContainerId);

		this.svg = this.navContainer
				.append("svg")
				.attr("class", "timeline__nav__container")
				.attr("width", "100%"); 

		let content = this.svg.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		this.eraContainer = content.append("g")
			.attr("width", "100%");
		this.hoverInfoContainer = content.append("g")
			.attr("width", "100%"); 
		this.dotContainer = content.append("g")
			.attr("width", "100%"); 
		
		let minDate = min(this.eventList, (d) => { return new Date(d.start_date); });
		let maxDate = max(this.eventList, (d) => { return d.end_date ? new Date(d.end_date) : new Date(d.start_date) });

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

		// if (this.eraList) {
		console.log("CHANGED!!");
		console.log(this.eraList);
			this.eraContainers = this.g.selectAll("g.timeline__nav__era-container")
				.data(this.eraList)
				.enter().append("g")
				.attr("class", "timeline__nav__era-container");

			console.log(this.eraContainers)

			this.eraDividers = this.eraContainers.append("line")
				.attr("class", "timeline__nav__era-divider")
				.attr("x1", 0)
				.attr("x2", 0)
				.attr("y1", 0);

			this.eraText = this.eraContainers.append("text")
				.attr("class", "timeline__nav__era-text")
				.text((d) => { console.log(d); return d.title; });

		// }

		this.currSelected = 0;

		this.contentContainer.select("#event-0").classed("visible", true);

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
		this.setEraContainers();
	}

	setWidth() {
		this.w = $(".timeline__nav").width() - margin.left - margin.right;

		this.g
			.attr("width", this.w);
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

		this.eventList.map((d) => {
			startXPos = this.xScale(new Date(d.start_date));
			endXPos = d.end_date ? this.xScale(new Date(d.end_date)) : startXPos;

			d.yIndex = this.calcYIndex(startXPos - dotRadius, endXPos + dotRadius);
			d.startXPos = startXPos;
			d.endXPos = endXPos;
			
		})

		this.numRows = this.rows.length;
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
			.data(this.eventList)
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

	setEraContainers() {
		this.eraContainers
			.attr("height", this.h + 2*(2*dotRadius + dotOffset))
			.attr("transform", (d) => { console.log(d); return "translate(" + this.xScale(new Date(d.start_date)) + ")"; });

		this.eraDividers
			.attr("height", 2*(2*dotRadius + dotOffset))
			.attr("y2", 2*(2*dotRadius + dotOffset))
			
	}

	setXAxis() {
		const [minTime, maxTime] = this.xScale.domain();
		let baseTopTransform = this.h + margin.top + dotRadius + dotOffset;

		let numTicks = this.w/100;
		let numDays = timeDay.count(minTime, maxTime),
			numMonths = timeMonth.count(minTime, maxTime),
			numYears = timeYear.count(minTime, maxTime);

		let dayMonth = {
			topTransform: baseTopTransform,
			tickSizeInner: 5,
		};
		
		let year = {
			topTransform: baseTopTransform + 20,
			tickValues: [minTime].concat(timeYear.range(minTime, maxTime)),
			tickFormat: timeFormat("%Y"),
			tickSizeInner: 0,
		};

		if (numDays/numTicks < 15) {
			dayMonth.tickValues = timeDay.range(minTime, maxTime, numDays/numTicks > 1 ? numDays/numTicks : 1 )
			dayMonth.tickFormat = timeFormat("%B %d")
		} else if (numDays/numTicks < 180) {
			console.log(numMonths, numTicks)
			console.log(numMonths/numTicks)
			dayMonth.tickValues = timeMonth.range(minTime, maxTime, numMonths/numTicks > 1 ? numMonths/numTicks : 1 )
			dayMonth.tickFormat = timeFormat("%B");
		} else {
			dayMonth.hidden = true;
			year.topTransform = baseTopTransform;
			year.tickSizeInner = 5;
			year.tickValues = timeYear.range(minTime, maxTime, numYears/numTicks > 1 ? numYears/numTicks : 1 )
		}

		this.renderAxis("day_month", dayMonth);
		this.renderAxis("year", year);
	}

	renderAxis(whichAxis, settings) {
		let {topTransform, tickValues, tickFormat, tickSizeInner, hidden, ticks} = settings;
		let axis = whichAxis == "year" ? this.yearAxis : this.dayMonthAxis;

		console.log(tickValues);
		let axisFunc = axisBottom(this.xScale)
			.tickPadding(5)
			.tickSizeOuter(0)
			.tickSizeInner(tickSizeInner)
			.tickFormat(tickFormat)
			.tickValues(tickValues);

		axis.style("display", hidden ? "none" : "block")
			.attr("transform", "translate(" + margin.left + "," + topTransform + ")")
			.call(axisFunc);
	}

	resize() {
		console.log("resizing");

		this.g.selectAll("rect").remove();

		this.render()
	}

	mouseover(datum, path) {
		console.log(this.numRows);
		let elem = select(path);
		elem.classed("hovered", true);

		this.hoverInfo
			.classed("hidden", false)
			.attr("transform", "translate(" + (elem.attr("x") + 30) + "," + this.yScale(this.numRows - 1) + ")");

		this.hoverInfoText.text(datum.title);
	}

	mouseout(path) {
		select(path).classed("hovered", false);

		this.hoverInfo.classed("hidden", true);
	}

	clicked(datum, path) {
		const { id } = datum;
		console.log("clicked!");
		this.contentContainer.select("#event-" + this.currSelected).classed("visible", false);
		// console.log(this.navContainer.select("#event-" + this.currSelected));
		this.navContainer.select(".timeline__nav__dot.selected").classed("selected", false);
		// console.log(this.navContainer.select(".timeline__nav__dot.selected"))
		this.currSelected = id;
		this.contentContainer.select("#event-" + id).classed("visible", true);
		select(path).classed("selected", true);
	}
}

export default function() {
	console.log("loaded script!");
	console.log(timelineEventSettings);
	let timelineDivs = $(".timeline");
	// let navContainers = timelineDivs.children(".timeline__nav"),
	// 	contentContainers = timelineDivs.children(".timeline__content");
	console.log(timelineDivs)
	let i = 0;
	for (let settingsObject of timelineEventSettings) {
		let navContainer = $(timelineDivs[i]).children(".timeline__nav")[0],
			contentContainer = $(timelineDivs[i]).children(".timeline__content")[0];
		console.log(settingsObject)
		new Timeline(settingsObject, navContainer, contentContainer);
		i++;
	}
	
	

	
}