const path = require("path");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");
const webpack = require("webpack");
const WebpackBabelExternalsPlugin = require('webpack-babel-external-helpers-2');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const NODE_ENV = process.env.NODE_ENV || 'development';

module.exports = {
  mode: NODE_ENV,
  entry: {
		"newamericadotorg": "./newamericadotorg/assets/newamericadotorg.js"
	},
  output: {
		filename: NODE_ENV == "development" ? "static/js/[name].js" : "static/js/[name]-[hash].js",
    chunkFilename: NODE_ENV == "development" ? "static/js/[name].js" : "static/js/[name]-[hash].js",
    publicPath: `${process.env.STATIC_URL || ''}/`,
    path: path.resolve(__dirname, "./newamericadotorg"),
    crossOriginLoading: "anonymous"
  },
  devtool: 'cheap-module-source-map',
  module: {
    rules: [
      {
        test: /\.scss/,
        use: [
					{
						loader: MiniCssExtractPlugin.loader,

					},
					'css-loader',
					{
						loader: 'sass-loader',
						options: {
							data: `$static: ${NODE_ENV==='development' ? '"/static"' : `"${process.env.STATIC_URL}/static"` };`
						}
					},
          {
            loader: 'sass-resources-loader',
            options: {
              resources: "./newamericadotorg/assets/scss/_mixins.scss"
            }
          }
				]
      },
      // {
      //   test: /\.js$/,
      //   exclude: /node_modules/,
      //   loaders: "eslint-loader",
      // },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loaders: "babel-loader",
        options: {
          presets: ["env", "react", "stage-0", "es2015"],
          plugins: ["transform-class-properties", "transform-object-rest-spread"]
        }
      }
    ]
  },
	optimization: {
    minimizer: [
      new UglifyJsPlugin({
        cache: true,
        parallel: true,
        sourceMap: true
      }),
      new OptimizeCSSAssetsPlugin({})
    ],
		splitChunks: {
      chunks: 'all',
      minSize: 10000,
			cacheGroups: {
        default: false,
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          enforce: true,
          chunks: 'all'
        }
			}
		}
  },
  plugins: [
		new MiniCssExtractPlugin({
      filename: "templates/style.css",
      chunkFilename: NODE_ENV == "development" ? "static/css/[name].css" : "static/css/[name]-[hash].css"
    }),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify(NODE_ENV)
    }),
    new HtmlWebpackPlugin({
      filename: 'templates/base.html',
      staticUrl: `${process.env.STATIC_URL || ''}/static`,
      template: 'newamericadotorg/templates/index.html',
      inject: false
    })
  ]
};
