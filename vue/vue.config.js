const { defineConfig } = require('@vue/cli-service')
const NodePolyfillPlugin = require("node-polyfill-webpack-plugin");

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    plugins: [new NodePolyfillPlugin()],
  },
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
    host:'0.0.0.0',
    port: 8090,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '/api': {
        target: 'http://localhost:2200', // 后端服务地址
        changeOrigin: true,
      },
      '/api/run-exe': {
        target: 'http://localhost:2200', // 指向Node.js服务的端口
        changeOrigin: true,
      }
    }
  },
})