const merge = require('webpack-merge')
const common = require('./webpack.common.js')
const ExtractTextWebpackPlugin = require('extract-text-webpack-plugin')

module.exports = merge(common, {
  output: {
    filename: 'js/[name].[chunkhash].js',
  },
})

module.exports.plugins.push(
  new ExtractTextWebpackPlugin('css/[name].[chunkhash].css'))
