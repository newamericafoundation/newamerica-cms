import babel from 'rollup-plugin-babel';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'
import uglify from 'rollup-plugin-uglify';

export default {
  input: 'newamericadotorg/assets/js/modules/timeline/index.js',
  output: {
    format: 'iife',
    name: 'timeline',
    file: 'newamericadotorg/static/js/timeline.js',
  },
  plugins: [
    // import node_module dependencies
    resolve(),
    // shim for dependencies that are not written with es6-style exports
    commonjs({
      include: [
        'node_modules/**'
      ]
    }),
    babel({ exclude: 'node_modules/**' })
  ]
};
