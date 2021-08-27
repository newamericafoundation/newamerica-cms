#!/bin/bash

set -o errexit
set -o nounset

celery -A newamericadotorg worker --loglevel=info # --broker=redis://127.0.0.1:6379/0
