var path = require('path'),
	webpack = require('webpack');

module.exports = {

	entry: './mysite/assets/js/mysite.js',

	output: {
		path: path.resolve('./mysite/static/js'),
		publicPath: 'http://localhost:8000/',
		filename: 'mysite.js'
	},

	resolve: {
		modulesDirectories: [ 'node_modules' ]
	},

	module: {
		loaders: [
		
			{
				test: /(\.js)|(\.jsx)$/,
				loader: 'babel-loader',
				exclude: /(node_modules|bower_components)/,
				query: {
					presets: [ 'es2015', 'stage-0' ]
				}
			},

			{
				test: /\.scss$/,
				loaders: [ 'style', 'css', 'sass' ]
			},

			{
				test: /\.jade$/,
				loaders: [ 'jade' ]
			}

		]
	}

}