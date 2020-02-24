Custom Content Management System (CMS) built for New America

## Dependencies

You may want to use tools like [pyenv](https://github.com/pyenv/pyenv) to manage your Python version and [nvm](https://github.com/nvm-sh/nvm) to manage your Node version.

- [Homebrew](http://brew.sh/)
- [Python 3 and pip](https://docs.python-guide.org/starting/install3/osx/), version noted in [.python-version](.python-version)
- [Node.js](https://medium.com/@kkostov/how-to-install-node-and-npm-on-macos-using-homebrew-708e2c3877bd), version noted in [.nvmrc](.nvmrc)
- [virtualenv](http://virtualenvwrapper.readthedocs.org/en/latest/index.html) (`pip install virtualenv`) or [venv](https://docs.python.org/3/library/venv.html)
- [postgres](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/)
- [aws-cli](https://aws.amazon.com/cli/) (`pip install awscli`). You'll need an account at [aws.amazon.com](https://aws.amazon.com/) with an 'iam' user set up which is configured in a later step on this README. [More information about awscli configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
- `na-cms.env` from the `Design` folder in Google Drive, which you should rename to `.env`
- Helpful but not required: `fixture.json` from the `Design` folder in Google Drive or a dump of the DB


## Back-end setup (without Vagrant)

See below for instructions on how to set up with Vagrant (easier).

### Virtual environment

Clone the github repo and change into the repo directory.

Set up your virtual environment
- (with virtualenv)
  ```bash
  virtualenv -p python3 venv
  ```
- (with venv)
  ```bash
  python -m venv venv
  ```

Activate your virtual environment 
```bash
source venv/bin/activate
```

### Install requirements
```bash
pip install -r requirements.txt
```

There are additional dependencies for the PDF Generator, Redis, and Celery that are installable with pip, install those with   

- (for MacOS)   
  ```bash
  npm run brew
  ```

- (for Ubuntu/Debian)  
  ```bash
  npm run apt
  ```

### Set up your database

Initialize postgres database if you haven't already
```bash
initdb -D /usr/local/var/postgres
```

Create a database called newamerica
```bash
createdb newamerica
```

- if you get an error about a missing port, make sure postgres is running in the background
  ```bash
  postgres -D /usr/local/var/postgres
  ```

Create a user called newamerica with some password:
```bash
psql -d newamerica -c "CREATE USER <<USERNAME>> WITH PASSWORD '<<PASSWORD>>';"
```

Download `na-cms.env` and `fixture.json` from the  `Design` folder in Google Drive and place them in the root of this project. 
Rename the environment variables file from `na-cms.env` to `.env` and update the DATABASE_URL in it with the Postgres URL indicating the password you set. 
Format for URL is `postgres://USER:PASSWORD@HOST:PORT/NAME`

Load your environment variables:
```bash
source .env
```

#### If you're using fixtures

Migrate your database:
```bash
./manage.py migrate
```

Remove default wagtail data by running:
```bash
./manage.py deletesite
```

Load the data from the fixture:
```bash
./manage.py loaddata fixture.json
```

#### If you're using a database dump (which you shouldn't be, but until [#1374](https://github.com/newamericafoundation/newamerica-cms/issues/1374) is resolved)

You can get a db dump from heroku;
make sure you drop your db then run `pg_restore` locally.
```bash
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U <<USERNAME>> -d <<DB_NAME>> <<PATH_TO_DUMP>>
```

If you get a note about psql permissions run the following 

```sql
psql <<DB_NAME>> -c "GRANT ALL ON ALL TABLES IN SCHEMA public to <<USERNAME>>;"
psql <<DB_NAME>> -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to <<USERNAME>>;"
psql <<DB_NAME>> -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to <<USERNAME>>;"
```

#### If you're using neither the fixtures nor a db dump

You'll have to manually create a homepage

```
HomePage.objects.create(path='/', depth=2, title='home', slug='home')
```

#### If you'd like your local instance to include images:
```bash
aws configure # makes sure you have your AWS Key and Secret handy
./manage.py downloadlocalimages
```
this will download images to `media/` in the project's root. These images are handled by s3 in production.

### Run the local server

If you didn't use the fixture, create a superuser
```bash
./manage.py createsuperuser
```

Run your local server:
```bash
./manage.py runserver
```

In your browser, go to the site (at [localhost:8000/admin](localhost:8000/admin)). 

If you used the fixture, log in with username: admin and password: password. These are the default credentials provided through the fixture.

#### Runing the server after initial setup

When you're running the project with everything, including the front-end, set up, you can use the following command to load `.env`, activate your virual environment, and run the server.

```bash
npm start
```

## Back-end setup with Vagrant

Make sure you have the latest version of Vagrant installed.
The base box only works with VirtualBox so you will need that too.

After cloning the site, run the following commands to set up the Vagrant box,
pull data from staging then launch the web server.

```bash
vagrant up
vagrant ssh
fab pull-staging-data
djrun
```

Note that `./manage.py` does work in the box if you want to use it that way,
it's been aliased to `dj` for convenience. The `djrun` command is an alias of
`./manage.py runserver 0.0.0.0:8000`.

Within Vagrant, all of PostgreSQL's utilities are all configured and `psql` is
configured to use the 'newamerica-cms' database by default.

## Front-end setup

Install front-end dependencies
```bash
npm install
```

Grab static assets (fonts, icons, etc.). This requires `aws configure` if you didn't run it earlier.
```bash
npm run get-static
```

Start webpack for development
```bash
npm run dev
```

### For production
To compile front-end assets in production, run the one-time command:
```bash
npm run build:production
```
