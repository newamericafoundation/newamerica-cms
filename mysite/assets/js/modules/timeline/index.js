import $ from 'jquery';

import { axisBottom } from 'd3-axis';
import { scaleLinear, scalePoint, scaleQuantize } from 'd3-scale';
import { extent, ascending, min, max } from 'd3-array';
import { select, selectAll, event } from 'd3-selection';
import { nest } from 'd3-collection';
import { timeFormat } from 'd3-time-format';
import { timeDay, timeMonth, timeYear } from 'd3-time';
let Hammer = require('hammerjs');

const formatDate = {
	day: timeFormat("%B %d, %Y"),
	month: timeFormat("%B %Y"),
	year: timeFormat("%Y")
}

const parseDate = (date) => {
	let convertedDate = new Date(date)
    return new Date(convertedDate.getUTCFullYear(), convertedDate.getUTCMonth(), convertedDate.getUTCDate()); 
}

const dotRadius = 7,
	dotOffset = 1.5,
	rowHeight = 2*(dotRadius + dotOffset),
	margin = { left: 15, right: 15, top: 20, bottom: 50},
	strokeColor = "#c0c1c3",
	strokeSelectedColor = "#2c2f35",
	fillColor = "#fff",
	fillSelectedColor = "#2c2f35";

class Timeline {
	constructor(settingsObject, fullContainerId, navContainerId, contentContainerId, showAllToggle) {
		console.log("This is happening!!!");
		console.log(Hammer);
		Object.assign(this, settingsObject);

		console.log(this.eventList);

		this.currSelected = 0;

		this.appendContainers(navContainerId, contentContainerId);
		this.appendAxes();
		this.initializeScales();

		let swipeHandler = new Hammer(contentContainerId);

		swipeHandler
			.on("swipeleft", (ev) => {
				this.setNewSelected(this.currSelected + 1, false);
			}).on("swiperight", (ev) => {
				this.setNewSelected(this.currSelected - 1, false);
			});

		this.contentContainer.select("#event-0").classed("visible", true);
		
		this.render();

		window.addEventListener('resize', this.resize.bind(this));

		this.keyListener = this.keyPressed.bind(this);

		this.nextContainer = this.contentContainer.select(".timeline__next")
			.on("click", () => { return this.setNewSelected(this.currSelected + 1, false); });
		this.prevContainer = this.contentContainer.select(".timeline__prev")
			.on("click", () => { return this.setNewSelected(this.currSelected - 1, false); });

		this.showingAll = false;
		select(showAllToggle)
			.on("click", () => {
				console.log()
				if (this.showingAll) {
					select(fullContainerId).classed("show-all", false);
					this.showingAll = !this.showingAll;
				} else {
					select(fullContainerId).classed("show-all", true);
					this.showingAll = !this.showingAll;
				}
			});


		this.eventContentVisibleWidth = this.contentContainer.select(".timeline__visible-event-window").style("width");
		this.contentContainer.selectAll(".timeline__event").style("width", this.eventContentVisibleWidth);

		this.setNextPrev();
	}

	appendContainers(navContainerId, contentContainerId) {
		this.navContainer = select(navContainerId)
			.on("mouseover", () => { window.addEventListener('keydown', this.keyListener); })
			.on("mouseout", () => { window.removeEventListener('keydown', this.keyListener); })
		    

		this.contentContainer = select(contentContainerId)
			.on("mouseover", () => { window.addEventListener('keydown', this.keyListener); })
			.on("mouseout", () => { window.removeEventListener('keydown', this.keyListener); })
			// .on("touchstart",() => { console.log(event); this.touchStartCoords = event.touches[0]; })
			// .on("touchmove", (a, b, c, d) => { console.log(this.touchStartCoords); })
			// .on("touchend", () => { this.touchStartCoords = null; })

			
		this.svg = this.navContainer
				.append("svg")
				.attr("class", "timeline__nav__container")
				.attr("width", "100%"); 

		this.g = this.svg.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		if (this.eraList) {
			this.eraContainers = this.g.selectAll("g.timeline__nav__era-container")
				.data(this.eraList)
				.enter().append("g")
				.attr("class", "timeline__nav__era-container")
				.on("mouseover", (d) => { console.log("mousing over!", d);});

			this.eraDividers = this.eraContainers.append("line")
				.attr("class", "timeline__nav__era-divider")
				.attr("x1", 0)
				.attr("x2", 0)
				.attr("y1", 5);

			this.eraText = this.eraContainers.append("text")
				.attr("class", "timeline__nav__era-text")
				.text((d) => { console.log(d); return d.title; })
				.classed("visible", (d) => { 
					console.log(this.eventList[this.currSelected]);
					if (d.end_date && this.eventList[this.currSelected].start_date > d.end_date) {
						return false;
					}
					return this.eventList[this.currSelected].start_date > d.start_date;
				});
		}

		let hoverInfoContainer = this.g.append("g")
			.attr("width", "100%")
			.attr("height", rowHeight)
			.attr("transform", this.eraList ? "translate(0," + rowHeight + ")" : "none");

		this.hoverInfo = hoverInfoContainer.append("text")
			.attr("class", "timeline__nav__hover-info")
			.classed("hidden", true);

		this.dotContainer = this.g.append("g")
			.attr("width", "100%")
			.attr("transform", this.eraList ? "translate(0," + rowHeight/2 + ")" : "translate(0," + rowHeight/2 + ")"); 
	}

	appendAxes() {
		this.dayMonthAxis = this.g.append("g")
			.attr("class", "timeline__nav__axis axis axis-x day-month-axis");

		this.yearAxis = this.g.append("g")
			.attr("class", "timeline__nav__axis axis axis-x year-axis");

	}

	initializeScales() {
		let minDate = min(this.eventList, (d) => { return parseDate(d.start_date); });
		let maxDate = max(this.eventList, (d) => { return d.end_date ? parseDate(d.end_date) : parseDate(d.start_date) });

		this.xScale = scaleLinear()
			.domain([minDate, maxDate]);

		this.yScale = scaleLinear();
	}

	render() {
		this.setWidth();
		this.setXScaleRange();
		this.setDotRows();
		this.setHeight();
		this.setCircles();
		this.setEraContainerXCoords();
		this.setXAxis();
	}

	setWidth() {
		this.w = $(".timeline__nav").width() - margin.left - margin.right;

		this.g
			.attr("width", this.w);
	}

	setXScaleRange() {
		this.xScale.range([0, this.w]);
	}

	setDotRows() {
		let startXPos, endXPos, yIndex;
		this.rows = [];
		this.rows[0] = [];

		this.eventList.map((d) => {
			startXPos = this.xScale(parseDate(d.start_date));
			endXPos = d.end_date ? this.xScale(parseDate(d.end_date)) : startXPos;

			d.yIndex = this.calcYIndex(startXPos - dotRadius, endXPos + dotRadius);
			d.startXPos = startXPos;
			d.endXPos = endXPos;
		})

		this.numDotRows = this.rows.length;

		this.yScale
			.domain([0, this.numDotRows])
			.range([this.numDotRows * rowHeight, 0]);
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

	setHeight() {
		let dotContainerHeight = this.numDotRows * rowHeight,
			gHeight = dotContainerHeight + rowHeight/2;

		gHeight += this.eraList ? rowHeight : 0;

		this.dotContainer.attr("height", dotContainerHeight);

		this.g.attr("height", gHeight);

		this.svg.attr("height", gHeight + margin.top + margin.bottom);

		this.dayMonthAxis.attr("transform", "translate(0," + gHeight + ")");
		this.yearAxis.attr("transform", "translate(0," + gHeight + ")");

		if (this.eraList) {
			this.eraContainers.attr("height", gHeight)
				
			this.eraDividers.attr("height", gHeight)
				.attr("y2", gHeight);
		}
	}

	setCircles() {
		this.circles = this.dotContainer.selectAll("rect")
			.data(this.eventList)
			.enter().append("rect")
		    .attr("x", (d) => { return d.startXPos - dotRadius; })
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

	setEraContainerXCoords() {
		let startX = 
		this.eraContainers
			.attr("transform", (d) => { return "translate(" + this.xScale(parseDate(d.start_date)) + ")"; })
			.attr("width", (d) => { return this.xScale(parseDate(d.end_date)) - this.xScale(parseDate(d.start_date)); });

		this.eraText
			.attr("x", (d) => { return (this.xScale(parseDate(d.end_date)) - this.xScale(parseDate(d.start_date)))/2 })
	}

	setXAxis() {
		const [minTime, maxTime] = this.xScale.domain();
		let baseTopTransform = this.numRows;

		let numTicks = this.w/100;
		let numDays = timeDay.count(minTime, maxTime),
			numMonths = timeMonth.count(minTime, maxTime),
			numYears = timeYear.count(minTime, maxTime);

		let dayMonth = {
			topTransform: 0,
			tickSizeInner: 5,
		};
		
		let year = {
			topTransform: 20,
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

		let axisFunc = axisBottom(this.xScale)
			.tickPadding(5)
			.tickSizeOuter(0)
			.tickSizeInner(tickSizeInner)
			.tickFormat(tickFormat)
			.tickValues(tickValues);

		axis.style("display", hidden ? "none" : "block")
			.call(axisFunc);
	}

	resize() {
		console.log("resizing");

		this.g.selectAll("rect").remove();

		this.eventContentVisibleWidth = this.contentContainer.select(".timeline__visible-event-window").style("width");
		this.contentContainer.selectAll(".timeline__event").style("width", this.eventContentVisibleWidth);
		this.contentContainer.select(".timeline__full-event-container")
			.style("transform", "translate(-" + (this.currSelected*this.eventContentVisibleWidth.replace("px", "")) + "px)");
		
		// let currEventHeight = this.contentContainer.select("#event-" + this.currSelected).style("height");
		// this.contentContainer.style("height", currEventHeight);
		console.log();

		this.render()
	}

	mouseover(datum, path) {
		console.log(this.numDotRows);
		let elem = select(path);
		elem.classed("hovered", true);

		this.hoverInfo
			.classed("hidden", false)
			.attr("transform", "translate(" + elem.attr("x") + ")")
			.text(datum.title);
	}

	mouseout(path) {
		select(path).classed("hovered", false);

		this.hoverInfo.classed("hidden", true);
	}

	clicked(datum, path) {
		const { id } = datum;
		this.setNewSelected(id, false);
	}

	setNewSelected(id, wrapAround) {
		console.log(this.currSelected);
		console.log(id);
		if (id < 0) {
			id = wrapAround ? this.eventList.length-1 : 0;
		} else if (id > this.eventList.length-1) {
			id = wrapAround ? 0 : this.eventList.length-1;
		}
		// let currEventHeight = this.contentContainer.select("#event-" + this.currSelected).style("height");
		// let nextEventHeight = this.contentContainer.select("#event-" + id).style("height");

		this.currSelected = id;

		this.contentContainer.select(".timeline__full-event-container").style("transform", "translate(-" + (id*this.eventContentVisibleWidth.replace("px", "")) + "px)");
		

		// if (currEventHeight > nextEventHeight) {
		// 	this.contentContainer.select(".timeline__full-event-container").style("transform", "translate(-" + (id*this.eventContentVisibleWidth.replace("px", "")) + "px)");
		// 	setTimeout(() => { 
		// 		this.contentContainer.style("height", nextEventHeight); 
		// 	}, 500);
		// } else {
		// 	this.contentContainer.style("height", nextEventHeight);
		// 	setTimeout(() => { 
		// 		this.contentContainer.select(".timeline__full-event-container").style("transform", "translate(-" + (id*this.eventContentVisibleWidth.replace("px", "")) + "px)");
		// 	}, 500);
		// }

		this.circles.classed("selected", (d) => { return d.id == this.currSelected });

		this.eraText
			.classed("visible", (d) => { 
				console.log(this.eventList[this.currSelected].start_date > d.start_date);
				if (d.end_date && this.eventList[this.currSelected].start_date > d.end_date) {
					return false;
				}
				return this.eventList[this.currSelected].start_date >= d.start_date;
			});
		
		// console.log(currEventHeight);
		

		this.setNextPrev();
	}

	keyPressed(eventInfo) {
		if (eventInfo.keyCode == 37) {
			this.setNewSelected(this.currSelected - 1, true);
		} else if (eventInfo.keyCode == 39) {
			this.setNewSelected(this.currSelected + 1, true);
		}
	}

	setNextPrev() {
		console.log("setting next prev");
		if (this.currSelected == 0) {
			this.prevContainer.classed("hidden", true);
			this.setNext();
			return;
		} 

		if (this.currSelected == this.eventList.length-1) {
			this.nextContainer.classed("hidden", true);
			this.setPrev();
			return;
		} 

		this.setNext();
		this.setPrev();
	}

	setNext() {
		const nextEvent = this.eventList[this.currSelected + 1];
		this.nextContainer.classed("hidden", false);
		this.nextContainer.select(".timeline__next-prev__date").text(this.formatDateLine(nextEvent));
		this.nextContainer.select(".timeline__next-prev__title").text(nextEvent.title);
	}

	setPrev() {
		const prevEvent = this.eventList[this.currSelected - 1];
		this.prevContainer.classed("hidden", false);
		this.prevContainer.select(".timeline__next-prev__date").text(this.formatDateLine(prevEvent));
		this.prevContainer.select(".timeline__next-prev__title").text(prevEvent.title);
	}

	formatDateLine(eventObject) {
		const { start_date, end_date, date_display_type } = eventObject;
		console.log(start_date);

		let retString = formatDate[date_display_type](parseDate(start_date));
		if (end_date) {
			let formattedEndString = formatDate[date_display_type](parseDate(end_date))
			retString += formattedEndString != retString ? " - " + formattedEndString : "";
		}

		return retString;
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
		let showAllToggle = $(timelineDivs[i]).children(".timeline__see-all-button")[0],
			navContainer = $(timelineDivs[i]).children(".timeline__nav")[0],
			contentContainer = $(timelineDivs[i]).children(".timeline__content")[0];
		console.log(settingsObject)
		new Timeline(settingsObject, timelineDivs[i], navContainer, contentContainer, showAllToggle);
		i++;
	}
	
	

	
}