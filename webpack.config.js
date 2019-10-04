const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer')
  .BundleAnalyzerPlugin;

const NODE_ENV = process.env.NODE_ENV || 'development';

module.exports = env => {
  return {
    mode: NODE_ENV,
    entry: {
      newamericadotorg: './newamericadotorg/assets/newamericadotorg.js',
      polyfills: './newamericadotorg/assets/polyfills.js'
    },
    output: {
      filename:
        NODE_ENV === 'development'
          ? 'static/js/[name].js'
          : 'static/js/[name]-[hash].js',
      chunkFilename:
        NODE_ENV === 'development'
          ? 'static/js/[name].js'
          : 'static/js/[name]-[hash].js',
      publicPath: `${process.env.STATIC_URL || ''}/`,
      path: path.resolve(__dirname, './newamericadotorg'),
      crossOriginLoading: 'anonymous'
    },
    devtool: 'source-map',
    module: {
      rules: [
        {
          test: /\.scss/,
          use: [
            {
              loader: MiniCssExtractPlugin.loader
            },
            'css-loader',
            {
              loader: 'sass-loader',
              options: {
                data: `$static: ${
                  NODE_ENV === 'development'
                    ? '"/static"'
                    : `"${process.env.STATIC_URL}/static"`
                };`
              }
            },
            {
              loader: 'sass-resources-loader',
              options: {
                resources: './newamericadotorg/assets/scss/_mixins.scss'
              }
            }
          ]
        },
        {
          test: /\.js$/,
          exclude: /node_modules/,
          loaders: 'babel-loader',
          options: {
            presets: [
              [
                '@babel/preset-env',
                {
                  targets: '> 1%, last 2 versions, Firefox ESR',
                  modules: false,
                  useBuiltIns: 'entry'
                }
              ],
              '@babel/preset-react'
            ],
            plugins: [
              '@babel/plugin-proposal-class-properties',
              '@babel/plugin-proposal-object-rest-spread',
              '@babel/plugin-syntax-dynamic-import'
            ]
          }
        }
      ]
    },
    optimization: {
      minimizer: [
        new TerserPlugin({
          parallel: true,
          sourceMap: true
        }),
        new OptimizeCSSAssetsPlugin({})
      ],
      splitChunks: {
        chunks(chunk) {
          return chunk.name !== 'polyfills';
        },
        maxInitialRequests: 6
      }
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename:
          NODE_ENV === 'development'
            ? 'static/css/[name].css'
            : 'static/css/[name]-[hash].css',
        chunkFilename:
          NODE_ENV === 'development'
            ? 'static/css/[name].css'
            : 'static/css/[name]-[hash].css'
      }),
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(NODE_ENV)
      }),
      new HtmlWebpackPlugin({
        filename: 'generated-templates/base.html',
        staticUrl: `${process.env.STATIC_URL || ''}/static`,
        template: 'newamericadotorg/templates/base.html',
        inject: false,
        serviceWorker: '/static/js/sw.js'
      }),
      NODE_ENV === 'development' && new BundleAnalyzerPlugin()
    ].filter(plugin => plugin)
  };
};
