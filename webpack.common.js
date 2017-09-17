var HtmlWebpackPlugin = require('html-webpack-plugin')
const ExtractTextWebpackPlugin = require('extract-text-webpack-plugin')

module.exports = {
  entry: {
    bootstrap: ['./static/js/bootstrap.js'],
    instantclick: ['./static/js/instantclick.js'],
  },
  output: {
    path: __dirname + '/dist',
    publicPath: '/static/',
  },
  module: {
    rules: [],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'templates/base.html',
      chunks: ['bootstrap'],
      inject: 'body',
      filename: 'base.html',
    }),
  ],
}
