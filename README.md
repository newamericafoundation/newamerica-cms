Custom Content Management System (CMS) built for New America

## Contents

- [First time setup](#first-time-setup)
- [Dependencies](#updating-dependencies)


## Setup

### Dependencies

This software should be installed on your computer:

1. [Docker](https://docs.docker.com/engine/installation/)

### First-time setup script

From inside the repo, run the setup script, which automates several steps needed to configure your environment so that the Docker containers can build successfully.

```shell
./setup.sh
```

### Starting the environment

This command will start the web, database, elastic search, and redis
servers needed for the site to operate:

```shell
docker compose up
```

The containers can also be run in detached mode with `docker compose up -d`.  In the default mode, you see all the logs and output from the containers in the shell and will stop running with Control+C.  Running with `-d` will cause docker compose to exit, but the containers will run in the background.  They can be stopped with `docker compose down`.  

The site will not immediately work without existing page data.  You can download this from the staging or production environments using Fabric commands.  Many of these commands require you be logged into Heroku, which you can do with this command:

```shell
docker compose exec web heroku login
```

Once the login is complete, you can use Fabric on the web container to obtain data from various sources.  For example:

```shell
docker compose exec web fab pull-production-data
```

Other Fabric commands can be listed with

```shell
docker compose exec web fab -l
```

### Visiting the site locally

After you have pull down data, you should be able to visit the Wagtail site at http://localhost:8000/

## Updating dependencies

The "docker build" command below will create new `requirements.txt` (for production -- Heroku requires this file to be in the root of the project folder hierarchy) and `requirements/local-dev.txt` (for development) and `requirements/ci.txt` (for use with continuous integration services) from the information in `pyproject.toml`.

```
docker build --target=requirements-artifacts -f ./docker/Dockerfile --output type=local,dest=. .
```

To change a requirement, update the version boundaries in the `project.dependencies` or appropriate key in `project.optional-dependencies` in `pyproject.toml` and re-run the docker build command.