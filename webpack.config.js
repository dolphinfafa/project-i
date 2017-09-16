var HtmlWebpackPlugin = require('html-webpack-plugin')
const ExtractTextWebpackPlugin = require('extract-text-webpack-plugin')

module.exports = {
  entry: {
    bootstrap: ['./static/js/bootstrap.js'],
  },
  output: {
    path: __dirname + '/dist',
    filename: 'js/bootstrap.js',
    publicPath: '/static/',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ExtractTextWebpackPlugin.extract({
          fallback: "style-loader",
          use: "css-loader"
        })
      }
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'templates/base.html',
      chunks: ['bootstrap'],
      inject: 'body',
      filename: 'base.html',
    }),
    new ExtractTextWebpackPlugin('css/bootstrap.css'),
  ],
}
