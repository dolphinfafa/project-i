var HtmlWebpackPlugin = require('html-webpack-plugin')
var CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = {
  entry: {
    layout: ['./static/js/layout.js'],
    home: ['./static/js/home.js'],
    blog: ['./static/js/blog.js'],
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
  copy: [
    // 邮件模板
    'customer/emails/',
    // Template Tags里使用到
    'catalogue/partials/product.html',
    'customer/history/recently_viewed_products.html',
    'promotions/default.html',
  ],
  // Chunk to template paths mapping
  mapping: {
    'home': ['cms/home_page.html'],
    'blog': [
      'blog/blog_index_page.html',
      'blog/blog_post_page.html',
    ],
    'layout': [
      'cms/custom_page.html',
    ],
    'oscar/layout': [
      '403.html',
      '404.html',
      '500.html',
      'login_forbidden.html',

      'basket/basket.html',

      'catalogue/browse.html',
      'catalogue/category.html',
      'catalogue/detail.html',

      'catalogue/reviews/review_detail.html',
      'catalogue/reviews/review_form.html',
      'catalogue/reviews/review_list.html',

      'checkout/checkout.html',
      'checkout/gateway.html',
      'checkout/payment_details.html',
      'checkout/preview.html',
      'checkout/shipping_address.html',
      'checkout/shipping_methods.html',
      'checkout/thank_you.html',
      'checkout/user_address_delete.html',
      'checkout/user_address_form.html',

      'customer/anon_order.html',
      'customer/login_registration.html',
      'customer/registration.html',

      'customer/address/address_delete.html',
      'customer/address/address_form.html',
      'customer/address/address_list.html',

      'customer/alerts/alert_list.html',
      'customer/alerts/form.html',

      'customer/email/email_detail.html',
      'customer/email/email_list.html',

      'customer/notifications/detail.html',
      'customer/notifications/list.html',

      'customer/order/order_detail.html',
      'customer/order/order_list.html',

      'customer/profile/change_password_form.html',
      'customer/profile/profile.html',
      'customer/profile/profile_delete.html',
      'customer/profile/profile_form.html',

      'customer/wishlists/wishlists_delete.html',
      'customer/wishlists/wishlists_delete_product.html',
      'customer/wishlists/wishlists_detail.html',
      'customer/wishlists/wishlists_form.html',
      'customer/wishlists/wishlists_list.html',

      'flatpages/default.html',

      'offer/detail.html',
      'offer/list.html',
      'offer/range.html',

      'promotions/automaticproductlist.html',
      'promotions/handpickedproductlist.html',
      'promotions/home.html',

      'registration/password_reset_complete.html',
      'registration/password_reset_confirm.html',
      'registration/password_reset_done.html',
      'registration/password_reset_form.html',

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
    'oscar/dashboard/login': [
      'dashboard/login.html',
    ],
  },
}

var i = TEMPLATES.copy.length
var copyconf = []
while (i--) {
  copyconf.push({
    from: TEMPLATES.root + TEMPLATES.copy[i],
    to: module.exports.output.path + '/' + TEMPLATES.copy[i],
  })
}

module.exports.plugins.push(new CopyWebpackPlugin(copyconf))

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
