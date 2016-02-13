import $ from 'jquery'

import addBorderPanelInteractivity from './plugins/index.js'

function addAllBorderPanelsInteractivity() {
	$('.border-panel').each((i, el) => {
		addBorderPanelInteractivity($(el))
	})
}

$(addAllBorderPanelsInteractivity)
