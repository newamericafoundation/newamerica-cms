import $ from 'jquery'

import './plug-ins/index.js'

function addAllBorderPanelsInteractivity() {
	$('.border-panel').each((i, el) => {
		$(el).addBorderPanelInteractivity()
	})
}

$(addAllBorderPanelsInteractivity)
