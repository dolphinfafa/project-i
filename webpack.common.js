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
      template: 'jingpai/templates/pages/home.html',
      chunks: ['bootstrap'],
      inject: 'body',
      filename: 'pages/home.html',
    }),
  ],
}
