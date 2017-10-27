const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: {
    main: './static/js/main.js',
    style: './static/css/main.less'
  },
  output: {
    path: path.resolve('./static/bundles/'),
    filename: '[name].js',
  },
  plugins: [
    new BundleTracker({ filename: './webpack-stats.json' }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
    }),
    new ExtractTextPlugin('styles.css'),
    //new UglifyJSPlugin(),
  ],

  module: {
    loaders: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          plugins: [
            'transform-runtime',
            'transform-react-remove-prop-types',
            'transform-react-constant-elements',
            'transform-react-inline-elements',
          ],
          presets: ['es2015', 'react'],
        }
      },

      {
       test: /\.css$/,
       loader: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader"})
      },

      {
        test: /\.less$/,
        loader: ExtractTextPlugin.extract({fallback: "style-loader", use: "css-loader!less-loader"})
      },
      {
    // I want to uglify with mangling only app files, not thirdparty libs
    test: /.*\/main\/.*\.js$/,
    exclude: /.spec.js/, // excluding .spec files
    loader: "uglify"
},
    ],
  },

  resolve: {
    modules: ['node_modules', 'bower_components'],
    extensions: ['.js', '.jsx'],
  },
};
