var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: './static/js/bootstrap.js',
  output: {
    path: __dirname+'/dist',
    filename: 'js/bootstrap.js',
    publicPath: '/',
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'templates/base.html',
      inject: 'body',
      filename: 'base.html',
    }),
  ],
}
