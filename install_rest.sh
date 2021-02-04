#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@d4e7a842abcc650f1d3c6614dfb93bf4f8b9c37f
