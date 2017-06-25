var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')
const ExtractTextPlugin = require("extract-text-webpack-plugin")

module.exports = {
  context: __dirname,

  entry: {main: './static/js/main.js', style: './static/css/main.less'},
  output: {
      path: path.resolve('./static/bundles/'),
      filename: "[name].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
    new ExtractTextPlugin('styles.css'),
  ],

  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          plugins: ['transform-runtime'],
          presets: ['es2015'],
        }
      }, // to transform JSX into JS
      {
    test: /\.css$/,
    loader: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader"})
},
// Optionally extract less files
// or any other compile-to-css language
{
    test: /\.less$/,
    loader: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader!less-loader"})
}
    ],
  },

  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['.js', '.jsx']
  },
}
