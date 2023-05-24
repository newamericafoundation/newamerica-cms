#!/bin/bash

# This script constructs the requirements files for our various
# environments from pyproject.toml.  Intended to be run during the
# docker build process for the web image.

set -e

python -m piptools compile --no-header --allow-unsafe --extra test --extra dev --resolver backtracking -o local-dev.txt pyproject.toml
python -m piptools compile --no-header --allow-unsafe --extra prod --resolver backtracking -o requirements.txt pyproject.toml
python -m piptools compile --no-header --allow-unsafe --extra test --resolver backtracking -o ci.txt pyproject.toml
