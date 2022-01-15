var baseConfig = require('./webpack.config.js');
var merge = require('webpack-merge');
var webpack = require('webpack');

module.exports = merge(baseConfig, {
    entry: [
        'webpack-dev-server/client?',
        'webpack/hot/only-dev-server'
    ],
    output: {
        publicPath: '/static/bundles/',
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoEmitOnErrorsPlugin(),
    ],
});
