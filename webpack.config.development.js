var path = require('path'),
	webpack = require('webpack'),
	baseConfig = require('./webpack.config.base.js');

module.exports = {
	entry: baseConfig.entry,
	output: baseConfig.output,
	resolve: baseConfig.resolve,
	module: baseConfig.module,
	plugins: baseConfig.plugins,
	devtool: 'source-map'
}