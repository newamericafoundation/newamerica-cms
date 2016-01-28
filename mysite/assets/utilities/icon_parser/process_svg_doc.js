import cheerio from 'cheerio'

export default function processSvgDoc(doc) {
	var $ = cheerio.load(doc, {
		normalizeWhitespace: false
	})
	$('*').attr('fill', null)
	$('*').attr('id', null)
	var $originSvg = $('svg')
	var viewBox = $originSvg.attr('viewbox')
	var innerHtml = $originSvg.html()
	var $newSvg = $(`<svg viewBox="${viewBox}"></svg>`).append(innerHtml)
	var $newSvgWrapper = $('<div></div>').append($newSvg)
	var svgHtml = $newSvgWrapper.html().replace(/viewbox/g, 'viewBox')
	return svgHtml
}