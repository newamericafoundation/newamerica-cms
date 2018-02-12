import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'
import replace from 'rollup-plugin-replace';

export default [
  {
    input: 'newamericadotorg/assets/js/dependencies.js',
    output: {
      file: 'newamericadotorg/static/js/dependencies.js',
      format: 'iife',
      name: 'dependencies'
    },
    onwarn: function(warn){
      return;
    },
    plugins: [
      replace({
        'process.env.NODE_ENV': '\'development\''
      }),
      resolve(),
      commonjs({
        include: [
          'node_modules/**'
        ],
        namedExports: {
          'node_modules/react/index.js': ['Children', 'Component', 'createElement', 'cloneElement'],
          'node_modules/react-dom/index.js': ['render'],
          'node_modules/date-fns/index.js': ['format']
        }
      })
    ]
  }
];
