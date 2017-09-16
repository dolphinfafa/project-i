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
      filename: 'base.html',
      template: 'templates/base.html',
    }),
  ],
}
