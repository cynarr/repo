#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@51cfae9ea92f10fa39be015c73900acff371c860
