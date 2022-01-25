const path = require('path');
const DST_PATH = '../pf_modeler/html/module/serve';

module.exports = {
  outputDir: path.resolve(__dirname, DST_PATH),
  configureWebpack: {
    output: {
      libraryExport: 'default',
    },
  },
  transpileDependencies: [],
};
