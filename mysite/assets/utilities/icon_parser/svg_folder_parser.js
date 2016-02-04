import fs from 'fs'
import SvgFileParser from './svg_file_parser.js'

export default class SvgFolderParser {

	constructor(options) {
		this.readPath = options.readPath
		this.writePath = options.writePath
		this._fileParsers = []
	}

	setIcons(next) {
		fs.readdir(__dirname + this.readPath, (err, files) => {
			if (err) { return next(err) }
			this._fileParsers = files.map((file) => {
				return new SvgFileParser({ 
					readPath: this.readPath + '/' + file,
					transform: 'normalize',
					writePath: this.writePath
				})
			})
			return next(this)
		})
		return this
	}

	parse(next) {
		var parsePromises = this._fileParsers.map(fileParser => fileParser.getParsePromise())
		Promise.all(parsePromises).then((results) => { console.log(results.join('\n\n')) }).catch((err) => { console.log(err.stack) })
	}

	parseAndWrite(next) {
		var parseAndWritePromises = this._fileParsers.map(fileParser => fileParser.getParseAndWritePromise())
		Promise.all(parseAndWritePromises).then((results) => {
			next('Good!')
		}).catch((err) => { 
			console.log(err.stack) 
			return next(err) 
		})
	}

}