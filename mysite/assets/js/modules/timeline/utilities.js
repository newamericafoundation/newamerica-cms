import { formatDate, parseDate } from "./constants";

export const formatDateLine = (eventObject) => {
	const { start_date, end_date, date_display_type } = eventObject;

	let retString = formatDate[date_display_type](parseDate(start_date));
	if (end_date) {
		let formattedEndString = formatDate[date_display_type](parseDate(end_date))
		retString += formattedEndString != retString ? " - " + formattedEndString : "";
	}

	return retString;
}

export const setColor = (d, colorScale) => {
	if (colorScale && d.category) {
		return colorScale(d.category);
	} else {
		return "rgba(138, 138, 138, 0.7)";
	}
}