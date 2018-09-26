Custom Content Management System (CMS) built for New America

### Dependencies

- [Homebrew](http://brew.sh/)
- [Python 3 and pip](https://docs.python-guide.org/starting/install3/osx/)
- [Node.js](https://medium.com/@kkostov/how-to-install-node-and-npm-on-macos-using-homebrew-708e2c3877bd)
- [virtualenv](http://virtualenvwrapper.readthedocs.org/en/latest/index.html) (`pip install virtualenv`)
- [postgres](http://exponential.io/blog/2015/02/21/install-postgresql-on-mac-os-x-via-brew/)
- [aws-cli](https://aws.amazon.com/cli/) (`pip install awscli`)

- Clone the github repo and change into the repo directory

### Wagtail/Django setup

- Set up your virtual environment
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

- Once inside the repo and your virtual environment, download na-cms.env and fixture.json from the [Design Drive](https://drive.google.com/drive/folders/1Fq2VaElPT1FuTFNUtXzyXyFX1a-9PlJK) and place them in the root of this project. You will need to customize the DATABASE_URL to match the database you will create shortly below.

- Install requirements:
```bash
pip install -r requirements.txt
```

- There are additional dependencies for the PDF Generator, Redis, and Celery that are installable with pip, install those with
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
source na-cms.env
```

- Migrate your database:
```bash
./manage.py migrate
```

- Remove default wagtail data by running:
```bash
./manage.py deletesite
```

- Load the data from the fixture:
```bash
./manage.py loaddata fixture.json
```

- If you'd like your local instance to include images:
```bash
aws configure # makes sure you have your AWS Key and Secret handy
./manage.py downloadlocalimages
```
this will download images to `media/` in the project's root. These images are handled by s3 in production.

- Run your local server:
```bash
./manage.py runserver
```

- In your browser, go to the site at (localhost:8000/admin) and log in with username: admin and password: password. These are the default credentials provided through the fixture.

### Install front-end

- Install front-end dependencies
```bash
npm install
```

- Grab static assets (fonts, icons, etc.):
```bash
npm run get-static
```

- start webpack for development
```bash
npm run dev
```

- To compile front-end assets in production, run the one-time command:
```bash
npm run build:production
```
