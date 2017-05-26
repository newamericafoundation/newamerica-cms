import babel from 'rollup-plugin-babel';
import replace from 'rollup-plugin-replace';

export default {
  entry: 'newamericadotorg/assets/js/newamericadotorg.js',
  dest: 'newamericadotorg/static/js/newamericadotorg.js',
  format: 'iife',
  moduleName: 'newamericadotorg',
  external: [
    'react', 'react-dom', 'prop-types', 'redux', 'react-redux', 'react-router',
    'react-router-dom', 'redux-thunk', 'date-fns', 'vanilla-lazyload', 'whatwg-fetch',
    'url-polyfill'
  ],
  globals: {
    'url-polyfill': 'URL',
    'whatwg-fetch': 'fetch',
    'react': 'React',
    'react-dom': 'ReactDOM',
    'prop-types': 'PropTypes',
    'redux': 'Redux',
    'react-redux': 'ReactRedux',
    'redux-thunk': 'ReduxThunk',
    'react-router': 'ReactRouter',
    'react-router-dom': 'ReactRouterDOM',
    'date-fns': 'dateFns',
    'vanilla-lazyload': 'LazyLoad',
  },
  plugins: [
    replace({
      'process.env.NODE_ENV': '\'' + process.env.NODE_ENV + '\'',
      'import \'./../scss/newamericadotorg.scss\';': ''
    }),
    babel(),
  ]
};
