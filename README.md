Custom Content Management System (CMS) built for New America

### Dependencies

- [Homebrew](http://brew.sh/)
- [Python 3 and pip](https://docs.python-guide.org/starting/install3/osx/)
- [Node.js](https://medium.com/@kkostov/how-to-install-node-and-npm-on-macos-using-homebrew-708e2c3877bd)
- [virtualenv](http://virtualenvwrapper.readthedocs.org/en/latest/index.html) (`pip install virtualenv`)
- [postgres](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/)

- Clone the github repo and change into the repo directory

### Wagtail/Django setup

- Set up your virtual environment
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

- Once inside the repo and your virtual environment, get a sample environment variables file from dev team and create your own environment variables file in your root directory (as in, where the manage.py file lives) named ".env". Copy paste contents from sample file here. You will need to customize the DATABASE_URL to match the database you will create shortly below.

- Install requirements:

```bash
pip install -r requirements.txt
```

There are additional dependencies for the PDF Generator, Redis, and Celery that are not python, install those with
```bash
npm run brew
```

- Initialize postgres database if you haven't already

```bash
initdb -D /usr/local/var/postgres
```

- Create a database called newamerica:
```bash
createdb newamerica
```
if you get an error about a missing port, make sure postgres is running in the background
```bash
postgres -D /usr/local/var/postgres
```

- Create a user called newamerica with some password:
```bash
psql -d newamerica -c "CREATE USER newamerica WITH PASSWORD '<<PASSWORD>>';"
```

- Update the DATABASE_URL in your environment variables file with the Postgres URL indicating the password you set. Format for URL is postgres://USER:PASSWORD@HOST:PORT/NAME

- Load your environment variables:
```bash
source .env
```

- Migrate your database:
```bash
python manage.py migrate
```

- Remove default wagtail data by running:
```bash
python manage.py deletedefaultwagtail
```

- Load the data from the fixture:
```bash
python manage.py loaddata fixture.json
```

- Run your local server:
```bash
python manage.py runserver
```

- In your browser, go to the site at (localhost:8000/admin) and log in with username: admin and password: admin. These are the default credentials provided through the fixture.


### Install front-end

```bash
npm install
```

To compile front-end assets in development and keep recompiling when any of the source files change, run the following:

```bash
npm run dev
```

To compile front-end assets in production, run the one-time command:

```bash
npm run build:production
```

### Images

The ``./newamericadotorg/assets/images`` folder contains images in development. In staging and production environments they are stored in s3 buckets on AWS.
