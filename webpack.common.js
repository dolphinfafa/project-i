var HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: {
    bootstrap: ['./static/js/bootstrap.js'],
    instantclick: ['./static/js/instantclick.js'],
    'oscar/layout': ['./static/oscar/js/layout.js'],
    'oscar/dashboard/layout': ['./static/oscar/js/dashboard/layout.js'],
    'oscar/dashboard/login': ['./static/oscar/js/dashboard/login.js'],
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
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        use: [
          'url-loader?limit=10000',
          'file-loader',
        ],
      },
    ],
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
      'catalogue/browse.html',
      'search/results.html',
    ],
    'oscar/dashboard/layout': [
      'dashboard/index.html',
    ],
    'oscar/dashboard/login':[
      'dashboard/login.html',
    ]
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
