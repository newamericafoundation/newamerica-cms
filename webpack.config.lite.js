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
		"newamericadotorg.lite": "./newamericadotorg/assets/newamericadotorg.lite.js"
	},
  output: {
		filename: "static/js/[name].js",
    path: path.resolve(__dirname, "./newamericadotorg"),
  },
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
							data: '$static: "https://d3fvh0lm0eshry.cloudfront.net/static";'
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
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "static/css/[name].css"
    }),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify(NODE_ENV)
    })
  ]
};
