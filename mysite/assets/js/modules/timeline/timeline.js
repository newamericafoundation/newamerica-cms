import $ from 'jquery';

import { axisBottom } from 'd3-axis';
import { scaleLinear, scalePoint, scaleQuantize, scaleOrdinal } from 'd3-scale';
import { extent, ascending, min, max } from 'd3-array';
import { select, selectAll, event } from 'd3-selection';
import { nest } from 'd3-collection';
import { timeFormat } from 'd3-time-format';
import { timeDay, timeMonth, timeYear } from 'd3-time';
import { transition } from 'd3-transition';
const Hammer = require('hammerjs');

import { dimensions, margin, parseDate } from './constants';
import { formatDateLine, setColor, whichEraOrSplit, isTouchDevice } from './utilities';

const subColor = "#b1b1b4";

export class Timeline {
	constructor(settingsObject, containerId) {
		Object.assign(this, settingsObject);
		this.fullEventList = this.eventList;
		this.currEventList = this.eventList;
		this.listView = false;
		this.currCategoryShown = "all";
		this.currSplitShown = "all";

		// if specific event id in url hash, sets that event as default
		let hashString = window.location.hash ? window.location.hash.replace("#", "") : null;
		if (hashString) {
			this.currSelected = this.getEventIndexByHash(hashString);
		} else {
			this.currSelected = 0;
		}
		

		this.cacheDOMSelections(containerId);
		this.appendContainers();

		if (this.splitList && this.splitList.length > 0) {
			// if specific event id in url hash, finds correct split to show, then filters events accordingly and finds curr event index in new list
			if (this.currSelected != 0) {
				this.currSplitShown = whichEraOrSplit(this.fullEventList[this.currSelected], this.splitList);
				this.filterEventList();
				this.currSelected = this.findNewEventIndex(this.currSelected);
				this.eventDivs
					.style("display", (d, i) => { return this.shouldShowEvent(this.fullEventList[i]) ? "block" : "none"; })
	
			} else {
				this.currSplitShown = this.splitList[0];
			}
			this.appendSplitButtons();
		}

		if (this.categoryList && this.categoryList.length > 0) { 
			this.initializeColorScale();
			this.appendCategoryLegend();
		}

		this.filterEventList();
		this.appendAxes();
		this.initializeXYScales();
		this.addListeners(containerId);
		this.render(true);
		this.setNextPrev();
	}

	//
	// initialization functions - called on first load
	//

	getEventIndexByHash(hash) {
		let decodedHash = decodeURI(hash).toLowerCase();

		let retIndex = 0;
		this.fullEventList.forEach((d, i) => {
			if (d.title.toLowerCase() === decodedHash) {
				retIndex = i;
				return;
			}
		})
		return retIndex;
	}

	cacheDOMSelections(containerId) {
		this.navContainer = select("#" + containerId + " .timeline__nav");
		this.categoryLegendContainer = select("#" + containerId + " .timeline__category-legend-container");
		this.contentContainer = select("#" + containerId + " .timeline__content");
		this.splitButtonContainer = select("#" + containerId + " .timeline__split-button-container");
		this.eventDivs = selectAll("#" + containerId + " .timeline__event");
	}

	appendContainers() {
		this.svg = this.navContainer
			.append("svg")
			.attr("class", "timeline__nav__container")
			.attr("width", "100%"); 

		this.g = this.svg.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

		this.eraList && this.eraList.length > 0 ? this.appendEraContainers() : null;

		let hoverInfoContainer = this.g.append("g")
			.attr("width", "100%")
			.attr("height", dimensions.rowHeight)
			.attr("transform", this.eraList && this.eraList.length > 0 ? "translate(0," + dimensions.rowHeight + ")" : "translate(0)");

		this.hoverInfo = hoverInfoContainer.append("text")
			.attr("class", "timeline__nav__hover-info")
			.classed("hidden", true);

		this.dotContainer = this.g.append("g")
			.attr("width", "100%")
			.attr("transform", this.eraList && this.eraList.length > 0 ? "translate(0," + dimensions.rowHeight/2 + ")" : "translate(0," + -dimensions.rowHeight/2 + ")"); 
	}

	appendSplitButtons() {
		let buttonList = this.splitButtonContainer.append("ul")
			.attr("class", "timeline__split-button-list");

		this.splitButtons = buttonList.selectAll("li")
			.data(this.splitList)
			.enter().append("li")
			.attr("class", "timeline__split-button")
			.classed("active", (d, i) => { return d == this.currSplitShown; })
			.on("click", (d, index, paths) => { this.changeSplitShown(d, index, paths); this.eventListChangedReRender();})
			.text((d) => { return d.title; });	
	}

	appendEraContainers() {
		this.eraContainers = this.g.selectAll("g.timeline__nav__era-container")
			.data(this.eraList)
			.enter().append("g")
			.attr("class", "timeline__nav__era-container");

		this.eraDividers = this.eraContainers.append("line")
			.attr("class", "timeline__nav__era-divider")
			.attr("x1", 0)
			.attr("x2", 0)
			.attr("y1", 5);

		this.eraText = this.g.append("text")
			.attr("class", "timeline__nav__era-text");

		this.addShowAllEraHeaders();
	}

	addShowAllEraHeaders() {
		let eventDivs = this.contentContainer.selectAll(".timeline__event")._groups[0];

		for (let era of this.eraList) {
			for (let i = 0; i < this.fullEventList.length; i++) {
				if (parseDate(this.fullEventList[i].start_date) >= parseDate(era.start_date)) {
					$("<h5 class='timeline__event__list-view-era-header'>" + era.title + " (" + formatDateLine(era, true) + ")</h5>")
						.insertBefore(eventDivs[i]);
					break;
				}
			}
		}
	}

	appendCategoryLegend() {
		const strokeWidth = 1;
		let categoryLegend = this.categoryLegendContainer.append("ul")
			.attr("class", "timeline__category-legend");

		this.categoryLegendItems = categoryLegend.selectAll("li")
			.data(this.categoryList)
			.enter().append("li")
			.attr("class", "timeline__category-legend__item active")
			.on("click", (category, index, paths) => { return this.changeCategoryFilter(category, index, paths);  });

		this.categoryLegendCircles = this.categoryLegendItems
		   .append("svg")
			.attr("class", "timeline__category-legend__color-swatch-container")
			.attr("height", 2*(dimensions.dotRadius + strokeWidth))
			.attr("width", 2*(dimensions.dotRadius + strokeWidth))
		   .append("circle")
			.attr("class", "timeline__category-legend__color-swatch")
			.attr("cx", dimensions.dotRadius + strokeWidth)
			.attr("cy", dimensions.dotRadius + strokeWidth)
			.attr("r", dimensions.dotRadius)
			.attr("stroke", (d) => { return setColor({"category": d}, this.colorScale); })
			.attr("fill", "white");

		this.categoryLegendText = this.categoryLegendItems
		   .append("h5")
			.attr("class", "timeline__category-legend__text")
			.style("color", (d) => { return setColor({"category": d}, this.colorScale); })
			.text((d) => { return d; });
	}

	appendAxes() {
		this.dayMonthAxis = this.g.append("g")
			.attr("class", "timeline__nav__axis axis axis-x day-month-axis");

		this.yearAxis = this.g.append("g")
			.attr("class", "timeline__nav__axis axis axis-x year-axis");
	}

	initializeXYScales() {
		let minDate = min(this.currEventList, (d) => { return parseDate(d.start_date); });
		let maxDate = max(this.currEventList, (d) => { return d.end_date ? parseDate(d.end_date) : parseDate(d.start_date) });

		this.xScale = scaleLinear()
			.domain([minDate, maxDate]);

		this.yScale = scaleLinear();
	}

	initializeColorScale() {
		this.colorScale = scaleOrdinal()
			.domain(this.categoryList)
			.range(["#2ebcb3", "#477da3", "#692025", "#2a8e88", "#5ba4da"]);
	}
	
	addListeners(containerId) {
		// adds arrow key listeners only when user is hovered over nav or content containers
		select("#" + containerId)
			.classed("touch", isTouchDevice())
			.on("mouseover", () => { window.addEventListener('keydown', this.keyListener); })
			.on("mouseout", () => { window.removeEventListener('keydown', this.keyListener); })   

		if (select("#" + containerId).classed("touch")) {
			console.log("this is a touch screen!");
			let swipeHandler = new Hammer($("#" + containerId)[0])
				.on("swipeleft", (ev) => {
					this.setNewSelected(this.currSelected + 1, false);
				}).on("swiperight", (ev) => {
					this.setNewSelected(this.currSelected - 1, false);
				});
		}

		window.addEventListener('resize', this.resize.bind(this));

		this.keyListener = this.keyPressed.bind(this);

		this.nextContainer = this.contentContainer.select(".timeline__next")
			.on("click", () => { return this.setNewSelected(this.currSelected + 1, false); });
		this.prevContainer = this.contentContainer.select(".timeline__prev")
			.on("click", () => { return this.setNewSelected(this.currSelected - 1, false); });

		select("#" + containerId + " .timeline__see-all-button")
			.on("click", () => {
				if (this.listView) {
					select("#" + containerId).classed("loading", true).classed("list-view", false);
					this.listView = !this.listView;
					this.resize();
					select("#" + containerId).classed("loading", false);
				} else {
					select("#" + containerId).classed("loading", true).classed("list-view", true);
					this.listView = !this.listView;
					this.resize();
					select("#" + containerId).classed("loading", false);
				}
			});
	}

	//
	// rendering functions - called on initialization and resize
	//

	render(shouldTransition) {
		this.setWidth();
		this.setDotRows();
		this.setHeight();
		this.setCircles();
		this.eraList && this.eraList.length > 0 ? this.setEraContainerXCoords() : null;
		this.setXAxis(shouldTransition);
	}

	setWidth() {
		this.w = $(".timeline__nav").width() - margin.left - margin.right;

		this.g
			.attr("width", this.w);

		this.eventContentVisibleWidth = this.contentContainer.select(".timeline__visible-event-window").style("width");
		this.contentContainer.selectAll(".timeline__event").style("width", this.eventContentVisibleWidth);
		this.contentContainer.select(".timeline__full-event-container")
			.style("transform", "translate(-" + (this.currSelected*this.eventContentVisibleWidth.replace("px", "")) + "px)");
	
		this.xScale.range([0, this.w]);
	}

	// performs layout calculations to avoid overlaps - stores 2D array of rows, with each row array storing the start and
	//		end positions of dots in that row, then uses this array to calculate y position for each point
	setDotRows() {
		let startXPos, endXPos, yIndex;
		this.rows = [];
		this.rows[0] = [];

		this.currEventList.map((d) => {
			startXPos = this.xScale(parseDate(d.start_date));
			endXPos = d.end_date ? this.xScale(parseDate(d.end_date)) : startXPos;

			d.yIndex = this.calcYIndex(startXPos - dimensions.dotRadius, endXPos + dimensions.dotRadius);
			d.startXPos = startXPos;
			d.endXPos = endXPos;
		})

		this.numDotRows = this.rows.length;

		this.yScale
			.domain([0, this.numDotRows])
			.range([this.numDotRows * dimensions.rowHeight, 0]);
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
		let dotContainerHeight = this.numDotRows * dimensions.rowHeight,
			gHeight = dotContainerHeight + dimensions.rowHeight/2;

		console.log(gHeight);
		gHeight += this.eraList && this.eraList.length > 0 ? dimensions.rowHeight : 0;
		console.log(gHeight);

		this.dotContainer.attr("height", dotContainerHeight);

		this.svg
			.transition().duration(1150)
			.attr("height", gHeight + margin.top + margin.bottom);

		this.g
			.transition().duration(1150)
			.attr("height", gHeight);

		this.dayMonthAxis.attr("transform", "translate(0," + gHeight + ")");
		this.yearAxis.attr("transform", "translate(0," + gHeight + ")");

		if (this.eraList && this.eraList.length > 0) {
			this.eraContainers.attr("height", gHeight)
				
			this.eraDividers.attr("height", gHeight)
				.attr("y2", gHeight);
		}
	}

	setCircles() {
		this.circles = this.dotContainer.selectAll("rect")
			.data(this.currEventList)
			.enter().append("rect")
		    .attr("x", (d) => { return d.startXPos - dimensions.dotRadius; })
		    .attr("y", (d) => { return this.yScale(d.yIndex) - dimensions.dotOffset; })
		    .attr("height", dimensions.dotRadius*2)
		    .attr("width", (d) => { return d.endXPos && (d.endXPos != d.startXPos) ? d.endXPos - d.startXPos + dimensions.dotRadius*2 : dimensions.dotRadius*2; })
		    .attr("rx", dimensions.dotRadius)
		    .attr("ry", dimensions.dotRadius)
		    .attr("stroke", (d) => { return setColor(d, this.colorScale); })
		    .attr("fill", (d) => { return setColor(d, this.colorScale); })
		    .attr("class", "timeline__nav__dot")
		    .classed("selected", (d, i) => { return i == this.currSelected })
		    .on("mouseover", (d, index, paths) => { return this.mouseover(d, paths[index]); })
		    .on("mouseout", (d, index, paths) => { return this.mouseout(paths[index]); })
		    .on("click", (d, index) => { return this.clicked(index); });
	}

	setEraContainerXCoords() {
		this.eraContainers
			.attr("transform", (d) => { 
				return "translate(" + this.setEraStart(d) + ")";
			})
			.attr("width", (d) => {
				return this.setEraWidth(d);
			});

		this.setEraText();
	}

	setEraStart(d) {
		let start = this.xScale(parseDate(d.start_date));
		if (start < 0) { start = 0; }
		return start; 
	}

	setEraWidth(d) {
		let start = this.xScale(parseDate(d.start_date));
		let end = d.end_date ? this.xScale(parseDate(d.end_date)) : this.xScale.range()[1];

		if (start < 0) { start = 0; }
		if (end > this.xScale.range()[1]) { end = this.xScale.range()[1]; }

		return end - start;
	}

	setEraText() {
		let currSelectedEvent = this.currEventList[this.currSelected];
		let currEra = whichEraOrSplit(currSelectedEvent, this.eraList);

		// if current event is within an era, show era text
		if (currEra) {
			this.eraText
				.classed("visible", true)
				.text(currEra.title + " (" + formatDateLine(currEra, true) + ")");
			
			// handles case where eratext goes off edge of viewport
			let textWidth = this.eraText._groups[0][0].getBBox().width;
			let xCoord = this.setEraStart(currEra) + this.setEraWidth(currEra)/2;

			if ((Number(xCoord) + textWidth/2) > this.w) {
				xCoord = this.w - textWidth/2 + 5;
			} else if ((Number(xCoord) - textWidth/2) < 0) {
				xCoord = textWidth/2;
			}
			this.eraText.attr("x", xCoord);
		} else {
			this.eraText.classed("visible", false);
		}
	}

	setXAxis(shouldTransition) {
		const [minTime, maxTime] = this.xScale.domain();
		let baseTopTransform = this.numRows;

		let numTicks = this.w/100;
		let numDays = timeDay.count(minTime, maxTime),
			numMonths = timeMonth.count(minTime, maxTime),
			numYears = timeYear.count(minTime, maxTime);

		// defaults for daymonth and year axes
		let dayMonth = { tickSizeInner: 5,  tickPadding: 5};
		let year = {
			tickValues: [minTime].concat(timeYear.range(minTime, maxTime)),
			tickFormat: timeFormat("%Y"),
			tickSizeInner: 0,
			tickPadding: 25
		};

		// sets ticks and display of daymonth and year axes based on number of days per tick
		if (numDays/numTicks < 15) {
			dayMonth.tickValues = timeDay.range(minTime, maxTime, numDays/numTicks > 1 ? numDays/numTicks : 1 )
			dayMonth.tickFormat = timeFormat("%B %d")
		} else if (numDays/numTicks < 180) {
			dayMonth.tickValues = timeMonth.range(minTime, maxTime, numMonths/numTicks > 1 ? numMonths/numTicks : 1 )
			dayMonth.tickFormat = timeFormat("%B");
		} else {
			dayMonth.hidden = true;
			year.tickPadding = 5;
			year.tickSizeInner = 5;
			year.tickValues = timeYear.range(minTime, maxTime, numYears/numTicks > 1 ? numYears/numTicks : 1 );
		}

		// renders both axes
		this.renderAxis("day_month", dayMonth, shouldTransition);
		this.renderAxis("year", year, shouldTransition);
	}

	renderAxis(whichAxis, settings, shouldTransition) {
		let {tickValues, tickFormat, tickSizeInner, tickPadding, hidden, ticks} = settings;
		let axis = whichAxis == "year" ? this.yearAxis : this.dayMonthAxis;

		let axisFunc = axisBottom(this.xScale)
			.tickPadding(tickPadding)
			.tickSizeOuter(0)
			.tickSizeInner(tickSizeInner)
			.tickFormat(tickFormat)
			.tickValues(tickValues);

		if (shouldTransition) {
			axis.style("display", hidden ? "none" : "block")
	            .transition().duration(1150)
				.call(axisFunc);
		} else {
			axis.style("display", hidden ? "none" : "block")
				.call(axisFunc);
		}
	}

	//
	// navigation functions
	//

	// wrapAround indicators whether should wrap to first event when at end of list, vice-versa.
	//		only arrow key events allow wraparound
	setNewSelected(newIndex, wrapAround) {
		if (newIndex < 0) {
			newIndex = wrapAround ? this.currEventList.length-1 : 0;
		} else if (newIndex > this.currEventList.length-1) {
			newIndex = wrapAround ? 0 : this.currEventList.length-1;
		}

		this.currSelected = newIndex;
		// transforms event container to show current event within viewport
		this.contentContainer.select(".timeline__full-event-container").style("transform", "translate(-" + (newIndex*this.eventContentVisibleWidth.replace("px", "")) + "px)");
		this.circles.classed("selected", (d, i) => { return i == this.currSelected });
		this.eraList && this.eraList.length > 0 ? this.setEraText() : null;
		this.setNextPrev();
		console.log(this.currEventList[newIndex])
		history.replaceState(undefined, undefined, "#" + encodeURI(this.currEventList[newIndex].title));
	}

	setNextPrev() {
		if (this.currSelected == 0) {
			this.prevContainer.classed("hidden", true);
			this.setNext();
			return;
		} 
		if (this.currSelected == this.currEventList.length-1) {
			this.nextContainer.classed("hidden", true);
			this.setPrev();
			return;
		} 
		this.setNext();
		this.setPrev();
	}

	setNext() {
		if (this.currEventList.length <= 1) { return; }

		const nextEvent = this.currEventList[this.currSelected + 1];
		this.nextContainer.classed("hidden", false);
		this.nextContainer.select(".timeline__next-prev__date").text(formatDateLine(nextEvent));
		this.nextContainer.select(".timeline__next-prev__title")
			.classed("italicize", nextEvent.italicize_title)
			.text(nextEvent.title);
	}

	setPrev() {
		const prevEvent = this.currEventList[this.currSelected - 1];
		this.prevContainer.classed("hidden", false);
		this.prevContainer.select(".timeline__next-prev__date").text(formatDateLine(prevEvent));
		this.prevContainer.select(".timeline__next-prev__title")
			.classed("italicize", prevEvent.italicize_title)
			.text(prevEvent.title);
	}

	//
	// event handlers
	//

	resize() {
		this.g.selectAll("rect").remove();
		this.render(false);
	}

	mouseover(datum, path) {
		let elem = select(path);
		elem.classed("hovered", true);
		let elemX = elem.attr("x");

		this.hoverInfo
			.classed("hidden", false)
			.classed("italicize", datum.italicize_title)
			.attr("fill", setColor(datum, this.colorScale))
			.text(datum.title);

		let textWidth = this.hoverInfo._groups[0][0].getBBox().width;

		// ensures hover text doesn't overflow off right edge of screen
		if (Number(elemX) + textWidth > this.w) {
			elemX = this.w - textWidth + 5;
		} 
			
		this.hoverInfo.attr("transform", "translate(" + elemX + ")")
	}

	mouseout(path) {
		select(path).classed("hovered", false);
		this.hoverInfo.classed("hidden", true);
	}

	clicked(index) {
		this.setNewSelected(index, false);
	}

	// handles arrow key interaction
	keyPressed(eventInfo) {
		if (eventInfo.keyCode == 37) {
			this.setNewSelected(this.currSelected - 1, true);
		} else if (eventInfo.keyCode == 39) {
			this.setNewSelected(this.currSelected + 1, true);
		}
	}

	changeCategoryFilter(newCategory, pathIndex, paths) {
		let elem = select(paths[pathIndex]);

		if (this.currCategoryShown == newCategory) {
			this.currCategoryShown = "all";
			this.categoryLegendItems.classed("active", true);
			this.categoryLegendCircles.attr("r", dimensions.dotRadius);
			this.categoryLegendText
				.style("color", (d) => { return setColor({"category": d}, this.colorScale); } )
		} else {
			this.currCategoryShown = newCategory;
			this.categoryLegendItems.classed("active", false);
			elem.classed("active", true);
			this.categoryLegendCircles
				.attr("r", (d) => { return d == newCategory ? dimensions.dotRadius : 0 })
			this.categoryLegendText
				.style("color", (d) => { return d == newCategory ? setColor({"category": d}, this.colorScale) : subColor } )
		}

		this.filterEventList();
		this.eventListChangedReRender();
	}

	changeSplitShown(newSplit, pathIndex, paths) {
		let elem = select(paths[pathIndex]);

		this.splitButtons.classed("active", false);
		elem.classed("active", true);

		this.currSplitShown = newSplit;
		this.filterEventList();
	}

	filterEventList() {
		this.currEventList = this.fullEventList.filter((d) => { 
			return this.shouldShowEvent(d);
		})
	}

	eventListChangedReRender() {
		this.g.selectAll("rect").remove();
		this.currSelected = 0;
		this.initializeXYScales();
		this.render(true);
		this.setNewSelected(0, false);

		this.eventDivs
			.style("display", (d, i) => { return this.shouldShowEvent(this.fullEventList[i]) ? "block" : "none"; })
	}

	shouldShowEvent(eventObject) {
		if (this.currCategoryShown == "all" || eventObject.category == this.currCategoryShown) {
			if (this.currSplitShown == "all") {
				return true;
			} else {
				if (this.currSplitShown.end_date && eventObject.start_date > this.currSplitShown.end_date) {
					return false;
				}
				if (eventObject.start_date >= this.currSplitShown.start_date) {
					return true;
				}
			}
		}
		return false;
	}

	findNewEventIndex(currIndex) {
		let newIndex = 0;
		for (let eventObject of this.currEventList) {
			if (eventObject.id == currIndex) {
				return newIndex;
			}
			newIndex++;
		}
		return currIndex;
	}
}

global.Timeline = Timeline;
