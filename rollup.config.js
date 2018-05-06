import babel from 'rollup-plugin-babel';
import sass from 'rollup-plugin-sass';
import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs'
import replace from 'rollup-plugin-replace';
import uglify from 'rollup-plugin-uglify';
import postcss from 'postcss'
import cssnano from 'cssnano';
import fs from 'fs';
import path from 'path';

var production = process.env.NODE_ENV == 'production';
var development = process.env.NODE_ENV == 'development';

export default [
  {
    input: 'newamericadotorg/assets/js/newamericadotorg.js',
    output: {
      format: 'iife',
      name: 'newamericadotorg',
      file: 'newamericadotorg/static/js/newamericadotorg-v1.0.1.min.js',
    },
    external: development && [
      'react', 'react-dom', 'react-redux', 'redux', 'redux-thunk',
      'react-router', 'react-router-dom', 'date-fns', 'react-slick',
      'react-scrollbar', 'react-transition-group', 'expirePlugin',
      'store', 'prop-types', 'vanilla-lazyload', 'whatwg-fetch',
      'url-polyfill', 'store/plugins/expire', 'smooth-scroll',
      'bowser', 'dom-to-image', 'babel-polyfill', 'react-document-meta',
      'history/createBrowserHistory', 'react-ga', 'react-recaptcha'
    ],
    watch: {
      clearScreen: false
    },
    // fetch polyfill should happen in window context
    moduleContext: { 'node_modules/whatwg-fetch/fetch.js': 'window' },
    onwarn: function(warn){
      // this doesn't matter
      if(warn.message=="'default' is not exported by 'node_modules/redux/es/index.js'") return;
    },
    plugins: [
      development && replace({
        'process.env.NODE_ENV': '\'' + process.env.NODE_ENV + '\'',
        'import \'./../scss/newamericadotorg.scss\';': '',
        'import \'./../scss/critical.scss\';': ''
      }),
      production && sass({
        output: 'newamericadotorg/static/css/newamericadotorg.css',
        insert: false,
        options: {
          includePaths: [
            'node_modules', // all for font-awesome
            'newamericadotorg/assets/scss/settings/' + process.env.NODE_ENV,
            'newamericadotorg/assets/scss'
          ]
        },

        output: function(styles, styleNodes) {
          postcss([cssnano({ discardUnused: false, zindex: false })])
            .process(styleNodes[0].content)
            .then(result => {
              var final = '{% load static from staticfiles %}';
              final += result.css.replace(/\/static\/(.+?\.(svg|otf|ttf|eot|woff))/g, "{% static '\$1' %}");
              writeFile(
                'newamericadotorg/templates/style.css',
                final
              );
            });
          postcss([cssnano({ discardUnused: false, zindex: false })])
            .process(styleNodes[1].content)
            .then(result => {
              writeFile(
                'newamericadotorg/static/css/newamericadotorg-v1.0.1.min.css',
                result.css
              );
            });
        }
      }),
      // import node_module dependencies
      production && resolve(),
      // shim for dependencies that are not written with es6-style exports
      production && commonjs({
        include: [
          'node_modules/**'
        ],
        namedExports: {
          'node_modules/react/index.js': ['Children', 'Component', 'createElement', 'cloneElement'],
          'node_modules/react-dom/index.js': ['render'],
          'node_modules/date-fns/index.js': ['format', 'subDays']
        }
      }),
      babel({ exclude: 'node_modules/**' }),
      production && replace({
        'process.env.NODE_ENV': '\'' + process.env.NODE_ENV + '\''
      }),
      production && uglify()
    ]
  }
];

function mkdirpath ( _path ) {
	var dir = path.dirname( _path );
	try {
		fs.readdirSync( dir );
	} catch ( err ) {
		mkdirpath( dir );
		fs.mkdirSync( dir );
	}
}

function writeFile ( dest, data ) {
	return new Promise( function ( fulfil, reject ) {
		mkdirpath( dest );

		fs.writeFile( dest, data, function (err) {
			if ( err ) {
				reject( err );
			} else {
				fulfil();
			}
		});
	});
}
