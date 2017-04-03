import { formatDate, parseDate } from "./constants";

export const formatDateLine = (eventObject, leaveOpenEnded) => {
	const { start_date, end_date, date_display_type } = eventObject;

	let retString = formatDate[date_display_type](parseDate(start_date));
	if (end_date) {
		let formattedEndString = formatDate[date_display_type](parseDate(end_date))
		retString += formattedEndString != retString ? " - " + formattedEndString : "";
	} else if (leaveOpenEnded) {
		retString += "-";
	}

	return retString;
}

export const setColor = (d, colorScale) => {
	if (colorScale && d.category) {
		return colorScale(d.category);
	} else {
		return "#b1b1b4";
	}
}

// no way to reliably detect touch screen (http://www.stucox.com/blog/you-cant-detect-a-touchscreen/), but this covers most cases
export const isTouchDevice = () => {
	return 'ontouchstart' in window || navigator.msMaxTouchPoints;
}

