var path = require('path'),
	webpack = require('webpack'),
	CompressionPlugin = require('compression-webpack-plugin'),
	baseConfig = require('./webpack.config.base.js');

module.exports = {

	entry: baseConfig.entry,
	output: baseConfig.output,
	resolve: baseConfig.resolve,
	module: baseConfig.module,

	plugins: baseConfig.plugins.concat([
		new webpack.optimize.UglifyJsPlugin({
			mangle: {
				except: [ '$super', '$', 'exports', 'require' ]
			}
		})
	])

}