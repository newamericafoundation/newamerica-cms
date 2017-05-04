import cheerio from 'cheerio'
import fs from 'fs'
import path from 'path'

import * as transforms from './transforms.js'

const SPLITTER = '-'


export default class SvgFileParser {

	constructor(options) {
		this.name = path.basename(options.readPath, '.svg')
		this.readPath = options.readPath
		this.writePath = options.writePath
		this.transform = options.transform
	}

	getName() {
		var nameParts = this.name.slice(2).split(SPLITTER)
		nameParts = nameParts.map((part) => {
			return part
			// return part.slice(0, 1).toUpperCase() + part.slice(1)
		})
		return nameParts.join('-')
	}

	getParsePromise() {
		return this.getSvgReadPromise().then((svg) => {
			return svg
		})
	}

	getParseAndWritePromise() {
		return this.getParsePromise().then((svg) => {
			var filePath = this.writePath + '/' + this.getName() + '.html'
			fs.writeFile(filePath, svg)
		})
	}

	getSvgReadPromise() {
		return new Promise((resolve, reject) => {
			fs.readFile(__dirname + this.readPath, 'utf-8', (err, doc) => {
				if (err) { return reject(err) }
				return resolve(transforms[this.transform](doc, this.getName()))
			})
		})
	}

}