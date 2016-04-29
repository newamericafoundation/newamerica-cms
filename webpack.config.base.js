var path = require('path'),
	webpack = require('webpack'),
	AssetsPlugin = require('assets-webpack-plugin'),
	autoprefixer = require('autoprefixer');

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
				loaders: [ 'style', 'css', 'sass' ]
			},

			{
				test: /\.jade$/,
				loaders: [ 'jade' ]
			},

			{
                test:   /\.css$/,
                loader: "style-loader!css-loader!postcss-loader"
            }

		]
	},
	postcss: [ autoprefixer({ browsers: ['> 1%', 'Chrome >= 46', 'ChromeAndroid >= 46', 'Firefox >= 38', 'FirefoxAndroid >= 38','Safari >= 7', 'iOS >= 7', 'Explorer >= 11', 'ExplorerMobile >= 11', 'last 2 Edge versions', 'last 2 Android versions', 'last 2 Opera versions'] }) ],

	plugins: [
		// new AssetsPlugin({ filename: 'mysite/static/js/rev-manifest.json', fullPath: false })
	]

}