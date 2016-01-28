require('babel-core/register');

var IconSvgFiles = require('./icon_svg_files.js').default;

function entryPoint() {
	// Entry point.
	new IconSvgFiles('/../../images/svg')
		.setIcons((iconSvgFiles) => {
			if (iconSvgFiles == null) { return }
			iconSvgFiles.getReactComponent((comp) => {
				console.log(comp)
			})
		});
}

entryPoint()