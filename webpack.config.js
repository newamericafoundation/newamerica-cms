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

	module: {
		rules: [
			{
				test: /(\.js)|(\.jsx)$/,
				loader: 'babel-loader',
				exclude: /node_modules\/(?!(foundation-sites)\/).*/,
				query: {
					presets: [ 'es2015', 'stage-0' ]
				}
			},
			{
				test: /\.scss$/,
				use: [
					{
						loader:'style-loader'
					},
					{
						loader: 'css-loader'
					},
					{
						loader: 'postcss-loader',
						options: {
							autoprefixer: {
								browsers: ['> 1%', 'Chrome >= 46', 'ChromeAndroid >= 46', 'Firefox >= 38', 'FirefoxAndroid >= 38','Safari >= 7', 'iOS >= 7', 'Explorer >= 11', 'ExplorerMobile >= 11', 'last 2 Edge versions', 'last 2 Android versions', 'last 2 Opera versions']
							}
						}
					},
					{
						loader: 'sass-loader'
					}
				]
			},
			{
				test: /\.css$/,
				loader: 'raw-loader'
			},
			{
				test: /\.jade$/,
				loader: 'jade-loader'
			}
		]
	},
	devtool: (process.env.NODE_ENV === 'development') ? 'source-map' : false,
	plugins: (process.env.NODE_ENV === 'development') ? [] : [
		new webpack.optimize.UglifyJsPlugin({
			sourceMap: true,
			compress: {
       			warnings: true
     		},
			mangle: {
				except: [ '$super', '$', 'exports', 'require' ]
			}
		})
	]
};
