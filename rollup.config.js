import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'
import replace from 'rollup-plugin-replace';
import uglify from 'rollup-plugin-uglify';
import postcss from 'postcss'
import cssnano from 'cssnano';
import fs from 'fs';

export default {
  entry: 'newamericadotorg/assets/js/newamericadotorg.js',
  dest: 'newamericadotorg/static/js/newamericadotorg.min.js',
  format: 'iife',
  moduleName: 'newamericadotorg',
  // fetch polyfill should happen in window context
  moduleContext: { 'node_modules/whatwg-fetch/fetch.js': 'window' },
  onwarn: function(warn){
    // this doesn't matter
    if(warn.message=="'default' is not exported by 'node_modules/redux/es/index.js'") return;
  },
  plugins: [
    sass({
      output: 'newamericadotorg/static/css/newamericadotorg.css',
      insert: false,
      options: {
        includePaths: [
          'node_modules', // all for font-awesome
          'newamericadotorg/assets/scss/settings/' + process.env.NODE_ENV,
          'newamericadotorg/assets/scss'
        ]
      },
      processor: css => {
        // minify
        postcss([cssnano()])
          .process(css)
          .then(result => {
            fs.writeFileSync('newamericadotorg/static/css/newamericadotorg.min.css',result.css);
          });
      }
    }),
    // import node_module dependencies
    resolve(),
    // shim for dependencies that are not written with es6-style exports
    commonjs({
      include: 'node_modules/**',
      namedExports: {
        'node_modules/react/react.js': ['Children', 'Component', 'createElement'],
        'node_modules/react-dom/index.js': ['render'],
        'node_modules/date-fns/index.js': ['format']
      }
    }),
    babel({ exclude: 'node_modules/**' }),
    replace({
      'process.env.NODE_ENV': '\'' + process.env.NODE_ENV + '\''
    }),
    uglify()
  ]
};
