const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  publicPath: "/",
  outputDir: "../dist",
  assetsDir: "static",
  indexPath: "../templates/index.html",
  transpileDependencies: true
})
