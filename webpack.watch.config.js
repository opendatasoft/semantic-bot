var baseConfig = require('./webpack.config.js');
var merge = require('webpack-merge');
var webpack = require('webpack');

module.exports = merge(baseConfig, {
    entry: [
        'webpack-dev-server/client?http://localhost:8080/',
        'webpack/hot/only-dev-server'
    ],
    output: {
        publicPath: 'http://localhost:8080/static/js/bundle/',
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
    ],
});