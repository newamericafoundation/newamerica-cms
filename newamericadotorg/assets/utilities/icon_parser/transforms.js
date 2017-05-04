import cheerio from 'cheerio'

function removeAttributes($, attributes) {
	for (let attribute of attributes) {
		$('*').attr(attribute, null)
	}
}

export function normalize(svgMarkup) {
	var $ = cheerio.load(svgMarkup, {
		normalizeWhitespace: false
	})
	removeAttributes($, [ 'fill', 'id' ])
	var $originSvg = $('svg')
	var viewBox = $originSvg.attr('viewbox')
	var innerHtml = $originSvg.html()
	var $newSvg = $(`<svg viewBox="${viewBox}"></svg>`).append(innerHtml)
	var $newSvgWrapper = $('<div></div>').append($newSvg)
	var svgHtml = $newSvgWrapper.html().replace(/viewbox/g, 'viewBox')
	return svgHtml
}

export function toReactComponent(svgMarkup, componentName = 'Component') {
	return `
export function ${componentName}() {
	return (
	${normalize(svgMarkup)}
	)
}
`
}