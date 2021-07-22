# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8-slim-buster

ARG DATABASE_URL
ARG USERID

# Add user that will be used in the container.
RUN useradd --uid $USERID wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DATABASE_URL="$DATABASE_URL"


RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    build-essential \
    git \
    libjpeg-dev \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libssl-dev \
    libz-dev \
    netcat \
    python3-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    gnupg2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Postgresql 13 client
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get -y install postgresql-client-13

# Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

RUN mkdir -p /home/wagtail
RUN chown wagtail:wagtail /home/wagtail

# Install the application server.
RUN pip install "gunicorn==20.0.4"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

COPY entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail
