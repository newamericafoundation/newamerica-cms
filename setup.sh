#!/usr/bin/env bash

set -e

# Needed so the docker containers have the correct filesystem permissions.
echo UID=$(id -u) > .env
echo GID=$(id -g) >> .env

# This file is needed to authenticate with Heroku.
touch ~/.netrc

# This directory is needed for the web container
mkdir -p static
