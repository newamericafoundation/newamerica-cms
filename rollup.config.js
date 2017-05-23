// import { rollup } from 'rollup';
import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'
import replace from 'rollup-plugin-replace';

export default {
  entry: 'newamericadotorg/assets/js/newamericadotorg.js',
  dest: 'newamericadotorg/static/js/newamericadotorg.js',
  format: 'iife',
  moduleName: 'newamericadotorg',
  globals: {},
  plugins: [
    sass({
      output: 'newamericadotorg/static/css/newamericadotorg.css',
      insert: false,
      options: {
        includePaths: [
          'node_modules',
          'newamericadotorg/assets/scss/settings/' + process.env.NODE_ENV,
          'newamericadotorg/assets/scss'
        ]
      }
    }),
    // shim for React that is not written with es6 exports
    commonjs({
      include: [
        'node_modules/**'
      ],
      exclude: [
        'node_modules/process-es6/**'
      ],
      namedExports: {
        'node_modules/react/react.js': ['Children', 'Component', 'PropTypes', 'createElement'],
        'node_modules/react-dom/index.js': ['render']
      }
    }),
    // import node_module dependencies
    resolve({
      jsnext: true,
      main: true,
      browser: true
    }),
    babel(),
    replace({
      'process.env.NODE_ENV': '\'' + process.env.NODE_ENV + '\''
    })
  ]
};
