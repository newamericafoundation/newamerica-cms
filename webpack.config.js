const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");
const WebpackBabelExternalsPlugin = require('webpack-babel-external-helpers-2');
//const HtmlWebpackPlugin = require('html-webpack-plugin');

const NODE_ENV = process.env.NODE_ENV || 'development';

module.exports = {
  mode: NODE_ENV,
  entry: {
		"newamericadotorg": "./newamericadotorg/assets/newamericadotorg.js",
    "newamericadotorg.lite": "./newamericadotorg/assets/newamericadotorg.lite.js"
	},
  output: {
		filename: "static/js/[name].js",
    chunkFilename: "static/js/[name].js",
    publicPath: '/',
    path: path.resolve(__dirname, "./newamericadotorg")
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
							data: `$static: ${NODE_ENV==='development' ? '"/static"' : '"https://s3.amazonaws.com/newamericadotorg-static/static"' };`
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
    minimize: false,
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
      chunkFilename: "static/css/[name].css"
    }),
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production")
    })
  ]
};
