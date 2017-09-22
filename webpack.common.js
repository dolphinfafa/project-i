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

      'dashboard/catalogue/category_delete.html',
      'dashboard/catalogue/category_form.html',
      'dashboard/catalogue/category_list.html',
      'dashboard/catalogue/product_class_delete.html',
      'dashboard/catalogue/product_class_form.html',
      'dashboard/catalogue/product_class_list.html',
      'dashboard/catalogue/product_delete.html',
      'dashboard/catalogue/product_list.html',
      'dashboard/catalogue/product_list.html',
      'dashboard/catalogue/product_update.html',
      'dashboard/catalogue/stockalert_list.html',

      'dashboard/comms/detail.html',
      'dashboard/comms/list.html',

      'dashboard/offers/benefit_form.html',
      'dashboard/offers/condition_form.html',
      'dashboard/offers/metadata_form.html',
      'dashboard/offers/offer_delete.html',
      'dashboard/offers/offer_detail.html',
      'dashboard/offers/offer_list.html',
      'dashboard/offers/restrictions_form.html',
      'dashboard/offers/step_form.html',

      'dashboard/orders/line_detail.html',
      'dashboard/orders/order_detail.html',
      'dashboard/orders/order_list.html',
      'dashboard/orders/shippingaddress_form.html',
      'dashboard/orders/statistics.html',

      'dashboard/pages/delete.html',
      'dashboard/pages/index.html',
      'dashboard/pages/update.html',

      'dashboard/partners/partner_delete.html',
      'dashboard/partners/partner_form.html',
      'dashboard/partners/partner_list.html',
      'dashboard/partners/partner_manage.html',
      'dashboard/partners/partner_user_form.html',
      'dashboard/partners/partner_user_list.html',
      'dashboard/partners/partner_user_select.html',

      'dashboard/promotions/delete.html',
      'dashboard/promotions/delete_pagepromotion.html',
      'dashboard/promotions/form.html',
      'dashboard/promotions/handpickedproductlist_form.html',
      'dashboard/promotions/page_detail.html',
      'dashboard/promotions/pagepromotion_list.html',
      'dashboard/promotions/promotion_list.html',

      'dashboard/ranges/range_delete.html',
      'dashboard/ranges/range_form.html',
      'dashboard/ranges/range_list.html',
      'dashboard/ranges/range_product_list.html',

      'dashboard/reports/index.html',

      'dashboard/reports/partials/offer_report.html',
      'dashboard/reports/partials/open_basket_report.html',
      'dashboard/reports/partials/order_report.html',
      'dashboard/reports/partials/product_report.html',
      'dashboard/reports/partials/submitted_basket_report.html',
      'dashboard/reports/partials/user_report.html',
      'dashboard/reports/partials/voucher_report.html',

      'dashboard/reviews/review_delete.html',
      'dashboard/reviews/review_list.html',
      'dashboard/reviews/review_update.html',

      'dashboard/shipping/weight_band_delete.html',
      'dashboard/shipping/weight_band_form.html',
      'dashboard/shipping/weight_based_delete.html',
      'dashboard/shipping/weight_based_detail.html',
      'dashboard/shipping/weight_based_form.html',
      'dashboard/shipping/weight_based_list.html',

      'dashboard/users/detail.html',
      'dashboard/users/index.html',

      'dashboard/users/alerts/delete.html',
      'dashboard/users/alerts/list.html',
      'dashboard/users/alerts/update.html',

      'dashboard/vouchers/voucher_delete.html',
      'dashboard/vouchers/voucher_detail.html',
      'dashboard/vouchers/voucher_form.html',
      'dashboard/vouchers/voucher_list.html',
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
