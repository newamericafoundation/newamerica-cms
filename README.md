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

To compile front-end assets, run the following:

	npm run dev

### Client-side JavaScript

The build procedure above allows client-side scripts to be built in CommonJS modules, which makes things easier to write, debug and test. It also allows ES6 features which allows us to skip semicolons and maintain scope while keeping code airy and pretty.