var HtmlWebpackPlugin = require('html-webpack-plugin')

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
      template: 'jingpai/templates/home/home_page.html',
      chunks: ['bootstrap'],
      inject: 'body',
      filename: 'home/home_page.html',
    }),
  ],
}
