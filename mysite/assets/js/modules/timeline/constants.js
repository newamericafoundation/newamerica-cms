import { timeFormat } from 'd3-time-format';
export const formatDate = {
	day: timeFormat("%B %d, %Y"),
	month: timeFormat("%B %Y"),
	year: timeFormat("%Y")
}

export const parseDate = (date) => {
	let convertedDate = new Date(date)
    return new Date(convertedDate.getUTCFullYear(), convertedDate.getUTCMonth(), convertedDate.getUTCDate()); 
}

export const margin = { left: 15, right: 15, top: 20, bottom: 25};

export const dimensions = {
	dotRadius : 7,
	dotOffset : 1.5,
};

dimensions.rowHeight = 2*(dimensions.dotRadius + dimensions.dotOffset);

// export const colors = {
// 	strokeColor : "#c0c1c3",
// 	strokeSelectedColor : "#2c2f35",
// 	fillColor : "#fff",
// 	fillSelectedColor : "#2c2f35"
// };

