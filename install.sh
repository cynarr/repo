#!/bin/bash

set -x trace -euo pipefail

poetry install
poetry run ./install_rest.sh
