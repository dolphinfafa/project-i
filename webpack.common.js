var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: {
    bootstrap: ['./static/js/bootstrap.js'],
    instantclick: ['./static/js/instantclick.js'],
    'oscar/layout': ['./static/oscar/js/layout.js'],
    'oscar/catalogue/browse': ['./static/oscar/js/catalogue/browse.js'],
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
      chunks: ['bootstrap'],
      inject: 'body',
      filename: 'home/home_page.html',
    }),
    new HtmlWebpackPlugin({
      template: 'jingpai/templates/promotions/home.html',
      chunks: ['oscar/layout'],
      inject: 'body',
      filename: 'promotions/home.html',
    }),
    new HtmlWebpackPlugin({
      template: 'jingpai/templates/catalogue/browse.html',
      chunks: ['oscar/catalogue/browse'],
      inject: 'body',
      filename: 'catalogue/browse.html',
    }),
    new HtmlWebpackPlugin({
      template: 'jingpai/templates/catalogue/category.html',
      chunks: ['oscar/layout'],
      inject: 'body',
      filename: 'catalogue/category.html',
    }),
  ],
}
