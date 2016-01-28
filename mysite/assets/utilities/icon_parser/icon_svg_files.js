import fs from 'fs'
import IconSvgFile from './icon_svg_file.js'

export default class IconSvgFiles {

	constructor(path) {
		this.path = path
	}

	getIconName(fileName) {
		return fileName.slice(6, -4)
	}

	setIcons(next) {
		this.list = []
		fs.readdir(__dirname + this.path, (err, files) => {
			if (err) { return next(err) }
			this.list = files.map((file) => {
				return new IconSvgFile({ 
					path: this.path + '/' + file
				})
			})
			return next(this)
		})
		return this
	}

	getReactComponent(next) {

		var output = ''
		var resolvedCount = 0

		this.list.forEach((iconSvgFile) => {

			iconSvgFile.getReactComponentDefinitionPromise().then((doc) => { 
				output += doc
				resolvedCount += 1
				// console.log(resolvedCount + ' -- ' + this.list.length);
				if (resolvedCount === this.list.length) {
					output = `import React from 'react'\n\n${output}`
					next(output);
				}
			}).catch((err) => { console.log(err.stack) })

		})

	}

}