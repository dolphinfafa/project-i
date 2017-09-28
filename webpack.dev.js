const merge = require('webpack-merge')
const common = require('./webpack.common.js')
const ExtractTextWebpackPlugin = require('extract-text-webpack-plugin')
const CleanWebpackPlugin = require('clean-webpack-plugin')
const OnlyIfChangedPlugin = require('only-if-changed-webpack-plugin')

module.exports = merge(common, {
  output: {
    filename: 'js/[name].js',
  },
  devtool: 'inline-source-map',
})

var lessrule = {
  test: /\.less/,
  use: ExtractTextWebpackPlugin.extract({
    fallback: 'style-loader',
    use: [
      {
        loader: 'css-loader',
      },
      {
        loader: 'less-loader',
      },
    ],
  }),
}

module.exports.module.rules.push(lessrule)

var cssrule = {
  test: /\.css$/,
  use: ExtractTextWebpackPlugin.extract({
    fallback: 'style-loader',
    use: 'css-loader',
  }),
}

module.exports.module.rules.push(cssrule)
module.exports.plugins.push(new ExtractTextWebpackPlugin('css/[name].css'))

var pathsToClean = [
  'dist/js',
  'dist/css',
  'build',
]

// the clean options to use
var cleanOptions = {
  root: __dirname,
  exclude: ['html5shiv.min.js'],
  verbose: true,
  dry: false,
}

module.exports.plugins.push(new CleanWebpackPlugin(pathsToClean, cleanOptions))

var opts = {
  rootDir: process.cwd(),
  devBuild: process.env.NODE_ENV !== 'production',
}

module.exports.plugins.push(new OnlyIfChangedPlugin({
  cacheDirectory: opts.rootDir + '/tmp/cache',
  cacheIdentifier: opts,  // all variable opts/environment should be used in cache key
}))
