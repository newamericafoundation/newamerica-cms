// import { rollup } from 'rollup';
import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';
// import resolve from 'rollup-plugin-node-resolve';
// import commonjs from 'rollup-plugin-commonjs'

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
    // resolve({
    //   jsnext: true,
    //   main: true,
    //   browser: true
    // }),
    babel()
  ]
};
