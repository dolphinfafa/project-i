const webpack = require('webpack');
const merge = require('webpack-merge')
const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
const common = require('./webpack.common.js')
const ExtractTextWebpackPlugin = require('extract-text-webpack-plugin')

module.exports = merge(common, {
  output: {
    filename: 'js/[name].[chunkhash].js',
  },
  devtool: 'source-map',
  plugins: [
    new UglifyJSPlugin({
      sourceMap: true,
    }),
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production'),
      },
    }),
  ],
})

module.exports.plugins.push(
  new ExtractTextWebpackPlugin('css/[name].[chunkhash].css'))