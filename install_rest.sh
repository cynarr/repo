#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@5ed9b804bf9434815e1783f17942aa8ae585907d
