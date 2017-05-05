import { rollup } from 'rollup';
import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';

export default {
  entry: 'newamericadotorg/assets/js/newamericadotorg.js',
  dest: 'newamericadotorg/static/js/newamericadotorg.js',
  format: 'iife',
  moduleName: 'widgetail',
  external: [
    'react',
    'react-dom',
    'redux',
    'react-redux',
    'axios',
    'redux-thunk'
  ],
  globals: {
    'react': 'React',
    'react-dom': 'ReactDOM',
    'axios': 'axios',
    'redux': 'Redux',
    'react-redux': 'ReactRedux',
    'redux-thunk': 'ReduxThunk'
  },
  plugins: [
    sass({
      output: 'build/widgetail.css',
      insert: true
    }),
    babel()
  ]
};
