#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@42b1ea7cfe859c05ee461ae59f463405378f69f8
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/newspaper.git@a097298e14ab0c79389ee1e445fc9f6c7dfc153f
