#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@a117c0f6c97a3ae72b08ccbd440a9fed52ac995a
