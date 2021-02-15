#!/bin/bash

set -x trace -euo pipefail

# Doesn't work with Poetry
pip install --ignore-installed --force-reinstall git+https://github.com/mood-mapping-muppets/news-please.git@42b1ea7cfe859c05ee461ae59f463405378f69f8
pip install --ignore-installed --force-reinstall git+https://github.com/mood-mapping-muppets/newspaper.git@a097298e14ab0c79389ee1e445fc9f6c7dfc153f
wget -o analysis/news_sentiment_model.bin https://a3s.fi/swift/v1/AUTH_d9eb9f26c2514801b54f21e00f15f5d4/mbert_news_sentiment/pytorch_model.bin
