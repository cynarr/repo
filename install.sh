#!/bin/bash

set -x trace -euo pipefail

poetry install $@
git submodule update --init --recursive
poetry run ./install_rest.sh
