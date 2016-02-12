Custom Content Management System (CMS) built for New America


# New America CMS Setup

- Install and create your virtual environment. One option: (http://virtualenvwrapper.readthedocs.org/en/latest/index.html)

- Clone github repo

- Get the requirements.txt and .env files from one of the developers and add both to your root directory of the CMS - as in, where the manage.py file lives

- Install pip if you don't have it: (https://pip.pypa.io/en/stable/installing/)

- Install Postgres and make sure it is running: (http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/)
Tip: Select the configuration to launch Postgres automatically so you don't have to do so manually each time you log in.

- Install requirements:
```bash
pip install -r requirements.txt
```

- Create a database called newamerica:
```bash
createdb newamerica
```

- Create a user called newamerica with some password:
```bash
psql -d newamerica -c "CREATE USER newamerica WITH PASSWORD '<<PASSWORD>>';"
```

- Updated the DATABASE_URL in the .env file with the Postgres url indicating the password you set. Format for URL is postgres://USER:PASSWORD@HOST:PORT/NAME


- Load your environment variables:
```bash
source .env
```


- Migrate your database:
```bash
python manage.py migrate
```

- Create a superuser:
```bash
python manage.py createsuperuser
```


- Run your local server:
```bash
python manage.py runserver
```

- In your browser, go to the site at (127.0.0.1:8000/admin) and log in with the credentials you created the super user with


- Delete the default “Welcome to your Wagtail site!” page


- Load the data from the fixture:
```bash
python manage.py loaddata fixture.json
```

- Run your local server:
```bash
python manage.py runserver
```

- In your browser, go to the site at (127.0.0.1:8000/admin) and log in with username: admin and password: admin



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

Note: ``npm run ...`` commands are shorthands for more complex commands mapped under the ``scripts`` key of ``package.json``.

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

### Images

The ``./mysite/assets/images`` folder contains images in development.

#### Icons

In the ``icons`` subfolder, there is a working Adobe Illustrator file with the current working version of all icons. Each icon occupies a single artboard, with lowercased name and with words separated by dashes.

Every time this file changes or new icons are added, the icons need to be recompiled, which is done as follows:

* save the icons as separate SVG's in the ``icons/svg`` subfolder. The individual filenames should start with ``i_``, followed by the name of the artboard and with a ``.svg`` extension (e.g. ``i_magnifying-glass.svg``). Illustrator saves in this format automatically if you set the save filename as ``i.svg``, and check the artboards as separate files box.
* run ``npm run get-icon-svgs``. This module will parse the files and ensures that the svg's are fully scalable, stylable and without unnecessary headers. It then copies them into ``/mysite/testserver/includes/svg``, removing the ``i_`` prefix. Note: the source code for this ``icon_parser`` module is under ``/mysite/assets/utilities/icon_parser`` - this is the module you'll need to modify if you change the folder structure or if something breaks with future versions of Node/npm.
* make sure that these files look right in the ``testserver`` folder. Then copy them into ``/mysite/templates/ui_elements/svg``, overriding as necessary. Automate this step if desired.
