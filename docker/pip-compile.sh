#!/bin/bash

# This script constructs requirements.txt and dev-requirements.txt
# from pyproject.toml.  Intended to be run during the docker build
# process for the web image.

set -e

python -m piptools compile --no-header --allow-unsafe --extra dev --resolver backtracking -o dev-requirements.txt pyproject.toml
python -m piptools compile --no-header --allow-unsafe --extra prod --resolver backtracking -o requirements.txt pyproject.toml


# pip-compile --generate-hashes --no-header --allow-unsafe --resolver=backtracking --output-file requirements.txt requirements.in

# pip-compile --generate-hashes --no-header --allow-unsafe --resolver=backtracking --output-file dev-requirements.txt dev-requirements.in
