# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.10-slim-buster AS python-base

RUN apt-get update && \
    apt-get install -y \
       gcc \
       libpq-dev \
       curl

FROM python-base AS builder
RUN pip install -U pip pip-tools wheel
COPY pyproject.toml ./
COPY docker/pip-compile.sh /usr/local/bin
COPY ./requirements/local-dev.txt ./
COPY ./requirements/prod.txt ./
COPY ./requirements/ci.txt ./
RUN pip-compile.sh

# This build target extracts the requirements.txt files from the
# previous stage and is intented to be used with
# `docker build --output=...`
FROM scratch AS requirements-artifacts
COPY --from=builder local-dev.txt ./requirements/local-dev.txt
COPY --from=builder prod.txt ./requirements/prod.txt
COPY --from=builder ci.txt ./requirements/ci.txt

FROM python-base

WORKDIR /root

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
    PORT=8000

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libjpeg-dev \
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
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Postgresql 13 client
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt buster-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get -y install postgresql-client-13

# Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

RUN mkdir -p /home/wagtail /opt/awscli
RUN chown wagtail:wagtail /home/wagtail

# AWS CLI
ADD https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip /root/awscliv2.zip
RUN unzip awscliv2.zip && ./aws/install -b /opt/awscli -i /opt/awscli && \
    rm -rf /opt/awscli/v2/current/dist/awscli/examples
RUN /opt/awscli/aws --version

COPY --from=builder local-dev.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

# Set this directory to be owned by the "wagtail" user. This Wagtail project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown wagtail:wagtail /app

COPY ./docker/entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/entrypoint.sh

COPY ./docker/django-start.sh /usr/local/bin
RUN chmod +x /usr/local/bin/django-start.sh

COPY ./docker/worker-start.sh /usr/local/bin
RUN chmod +x /usr/local/bin/worker-start.sh

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

ENV PATH="/opt/awscli:$PATH"

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
