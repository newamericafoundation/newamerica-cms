import $ from 'jquery';

import { Timeline } from './timeline';

export default function() {
	let timelineDivs = $(".timeline");

	let i = 0;
	for (let settingsObject of timelineEventSettings) {
		let elem = $(timelineDivs[i]);
		let showAllToggle = elem.children(".timeline__see-all-button")[0],
			navContainer = elem.children(".timeline__nav")[0],
			contentContainer = elem.children(".timeline__content")[0];

		new Timeline(settingsObject, timelineDivs[i], navContainer, contentContainer, showAllToggle);
		i++;
	}
}