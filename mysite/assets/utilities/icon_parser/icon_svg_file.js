import cheerio from 'cheerio'
import fs from 'fs'
import path from 'path'

import processSvgDoc from './process_svg_doc.js'

const SPLITTER = '_'



export default class IconSvgFile {

	constructor(options) {
		this.name = path.basename(options.path, '.svg')
		this.path = options.path
	}

	getReactComponentName() {
		var nameParts = this.name.split(SPLITTER)
		nameParts = nameParts.map((part) => {
			return part.slice(0, 1).toUpperCase() + part.slice(1)
		})
		return nameParts.join('')
	}

	getReactComponent(componentName, renderMarkup) {
		if (componentName == null || componentName === "") { return '' }
		return `
export function ${componentName}() {
	return (
	${renderMarkup}
	)
}
`
	}

	getReactComponentDefinitionPromise() {
		return this.getSvgReadPromise().then((svg) => {
			return this.getReactComponent(this.getReactComponentName(), svg)
		})
	}

	getSvgReadPromise() {
		return new Promise((resolve, reject) => {
			fs.readFile(__dirname + this.path, 'utf-8', (err, doc) => {
				if (err) { return reject(err) }
				return resolve(processSvgDoc(doc))
			})
		})
		
	}

}