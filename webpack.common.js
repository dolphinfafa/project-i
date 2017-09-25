var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: {
    home: ['./static/js/home.js'],
    instantclick: ['./static/js/instantclick.js'],
  },
  output: {
    path: __dirname + '/dist',
    publicPath: '/static/',
  },
  module: {
    rules: [
      // the url-loader uses DataUrls.
      // the file-loader emits files.
      {
        test: /\.woff(2)?(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff',
      },
      {
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=application/octet-stream',
      },
      {
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'file-loader',
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'url-loader?limit=10000&mimetype=image/svg+xml',
      },],
    loaders: [],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: 'jingpai/templates/home/home_page.html',
      chunks: ['home'],
      inject: 'body',
      filename: 'home/home_page.html',
    }),
  ],
}
