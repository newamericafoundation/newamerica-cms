const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');

module.exports = {

	entry: './mysite/assets/js/mysite.js',

	output: {
		path: path.resolve('./mysite/static/js'),
		publicPath: 'http://localhost:8000/',
		filename: 'mysite.js',
		sourceMapFilename: 'mysite.js.map'
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
				loaders: [ 'style', 'css', 'postcss', 'sass' ]
			},

			{
				test: /\.css$/,
				loaders: [ 'raw' ]
			},

			{
				test: /\.jade$/,
				loaders: [ 'jade' ]
			}

		]
	},
	postcss: [
		autoprefixer({
			browsers: ['> 1%', 'Chrome >= 46', 'ChromeAndroid >= 46', 'Firefox >= 38', 'FirefoxAndroid >= 38','Safari >= 7', 'iOS >= 7', 'Explorer >= 11', 'ExplorerMobile >= 11', 'last 2 Edge versions', 'last 2 Android versions', 'last 2 Opera versions']
		})
	],
	devtool: (process.env.NODE_ENV === 'development') ? 'source-map' : null,
	plugins: (process.env.NODE_ENV === 'development') ? [] : [
		new webpack.optimize.UglifyJsPlugin({
			mangle: {
				except: [ '$super', '$', 'exports', 'require' ]
			}
		})
	]
};
