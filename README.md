Custom Content Management System (CMS) built for New America


Install
-----------------

Install dependencies

    pip install -r requirements.txt


Set up
-----------------

    manage.py createsuperuser
    manage.py makemigrations
    manage.py migrate


Run
-----------------

    manage.py runserver


Front-end
-----------------

Front-end assets are developed in the ``./mysite/assets`` folder and compiled into ``./mysite/static`` using ``webpack``. Note that ``webpack`` bundles together CSS and JS to optimize page load, so the ``./mysite/static/css`` folder is not needed.

To contribute to frontend development, you need to install a ``Node.js`` environment, which is best handled using [Homebrew](http://brew.sh/). Once installed, run the following from project root:

	brew install node
	npm install

To compile front-end assets in development and keep recompiling when any of the source files change, run the following:

	npm run dev

To compile front-end assets in production, run the one-time command:

	npm run build

### Frontend test server

There is a separate, tiny Express server used solely to test HTML and CSS without the need to have Python, Django or Postgres configured. Run it by simply typing:

	npm run testserver

Its code is under ``/mysite/testserver``.

### Stylesheets

Development stylesheets are found under ``/mysite/assets/scss``.

Basic styling, grid and smaller UI elements are handled by Foundation 6, built from SASS by appropriately overriding Foundation's variables and only including the Foundation styles that the project needs. Normalize.css is used to work out differences between browsers' default styles. Both of these libraries are imported and/or customized in the ``/vendor`` subfolder.

Higher-level UI elements are called modules and have their custom styling. These custom styles follow [BEM naming conventions](http://getbem.com/introduction/), and the organization is largely inspired by [SMACSS](https://smacss.com/). For the most part, selectors are simple class names, and nesting is avoided unless it clearly expresses design intent (all ``.button`` elements within ``.header`` should have this override), or if it would result in too long class names (``.section__image__attribution__close-button``). If the latter comes up, it is best to factor out a sub-element into its own module.

### Client-side JavaScript

The build procedure above allows client-side scripts to be built in CommonJS modules, which makes things easier to write, debug and test. It also allows ES6 features which allows us to skip semicolons and maintain scope while keeping code airy and pretty.