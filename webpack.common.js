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
  plugins: [],
}

const TEMPLATES = {
  root: 'jingpai/templates/',
  inject: 'body',
  // Chunk to template paths mapping
  mapping: {
    'bootstrap': ['home/home_page.html'],
    'oscar/layout': [
      'promotions/home.html',
      'catalogue/category.html',
      'catalogue/detail.html',
      'catalogue/reviews/review_form.html',
      'offer/list.html',
      'customer/wishlists/wishlists_form.html',
    ],
    'oscar/catalogue/browse': [
      'catalogue/browse.html',
    ],
  },
}

for (var chunk in TEMPLATES.mapping) {
  var i = TEMPLATES.mapping[chunk].length
  while (i--) {
    var path = TEMPLATES.mapping[chunk][i]
    module.exports.plugins.push(new HtmlWebpackPlugin({
      template: TEMPLATES.root + path,
      chunks: [chunk],
      inject: TEMPLATES.inject,
      filename: path,
    }))
  }
}
