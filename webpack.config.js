var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: {
    bootstrap: ['./static/js/bootstrap.js'],
  },
  output: {
    path: __dirname + '/dist',
    filename: 'js/bootstrap.js',
    publicPath: '/static/',
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
