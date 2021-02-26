#!/bin/sh
set -xe

PROJECT_NAME=$1

PROJECT_DIR=/vagrant
VIRTUALENV_DIR=/home/vagrant/.virtualenvs/$PROJECT_NAME

PYTHON=$VIRTUALENV_DIR/bin/python
PIP=$VIRTUALENV_DIR/bin/pip


# Install Cairo, Pango and GDK-Pixbuf
apt-get update -y
apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0


# Replace Elasticsearch with version 2
echo "Downloading Elasticsearch..."
set +e
apt-get remove -y --purge elasticsearch
set -e
wget -q https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.deb
dpkg -i elasticsearch-5.6.16.deb

# Enable script scoring
cat << EOF >> /etc/elasticsearch/elasticsearch.yml
script.inline: on
script.search: on
EOF

# Reduce memory to fit in default virtualvox vm
sed -i 's/^\-Xms.*/\-Xms512m/' /etc/elasticsearch/jvm.options
sed -i 's/^\-Xmx.*/\-Xmx512m/' /etc/elasticsearch/jvm.options

systemctl enable elasticsearch
systemctl start elasticsearch

# Create database (let it fail because database may exist)
set +e
su - vagrant -c "createdb $PROJECT_NAME"
set -e


# Virtualenv setup for project
su - vagrant -c "virtualenv --python=python3 $VIRTUALENV_DIR"

su - vagrant -c "echo $PROJECT_DIR > $VIRTUALENV_DIR/.project"


# Upgrade PIP itself
su - vagrant -c "$PIP install --upgrade pip"

# Upgrade setuptools (for example html5lib needs 1.8.5+)
su - vagrant -c "$PIP install --upgrade six setuptools"

# Install PIP requirements
su - vagrant -c "cd $PROJECT_DIR && $PIP install -r requirements.txt"

# Install Fabric 2
apt-get remove -y fabric
su - vagrant -c "$PIP install Fabric==2.1.3"

# Set execute permissions on manage.py as they get lost if we build from a zip file
chmod a+x $PROJECT_DIR/manage.py


# running migrations here is typically not necessary because of fab pull_data
# su - vagrant -c "$PYTHON $PROJECT_DIR/manage.py migrate --noinput"

# Install Heroku CLI
curl -sSL https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install AWS CLI
apt-get update -y
apt-get install -y unzip
rm -rf /tmp/awscli-bundle || true
rm -rf /tmp/awscli-bundle.zip || true
curl -sSL "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "/tmp/awscli-bundle.zip"
unzip -q /tmp/awscli-bundle.zip -d /tmp
/tmp/awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws

# Add a couple of aliases to manage.py into .bashrc
cat << EOF >> /home/vagrant/.bashrc
export PYTHONPATH=$PROJECT_DIR
export DJANGO_SETTINGS_MODULE=newamericadotorg.settings.dev
export DATABASE_URL=postgres:///$PROJECT_NAME
export REDIS_URL=redis://localhost/1
export PGDATABASE=$PROJECT_NAME
export SECRET_KEY=test
export ELASTICSEARCH_URL=http://localhost:9200

alias dj="django-admin.py"
alias djrun="dj runserver 0.0.0.0:8000"
alias djrunp="dj runserver_plus 0.0.0.0:8000"

source $VIRTUALENV_DIR/bin/activate
export PS1="[$PROJECT_NAME \W]\\$ "
cd $PROJECT_DIR
EOF
