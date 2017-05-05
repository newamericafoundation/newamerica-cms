import { rollup } from 'rollup';
import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'

export default {
  entry: 'newamericadotorg/assets/js/newamericadotorg.js',
  dest: 'newamericadotorg/static/js/newamericadotorg.js',
  format: 'iife',
  moduleName: 'newamericadotorg',
  globals: {},
  plugins: [
    sass({
      output: 'newamericadotorg/static/css/newamericadotorg.css',
      insert: true
    }),
    resolve({
      jsnext: true,
      main: true,
      browser: true
    }),
    commonjs({
      namedExports: {
          'node_modules/jquery/dist/jquery.min.js': [ 'jquery' ]
      }
    }),
    babel()
  ]
};
