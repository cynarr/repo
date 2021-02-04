FROM quay.io/jitesoft/debian:10-slim

RUN apt-get update && \
    apt-get install -y zstd git python3 python3-dev python3-pip build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade \
    pip==20.2.4 \
    setuptools==50.3.2 \
    poetry==1.1.4

WORKDIR /opt/coviddash

COPY pyproject.toml poetry.lock install_rest.sh ./

RUN poetry export \
      --without-hashes > requirements.txt && \
    python3 -m pip install -r requirements.txt && \
    rm requirements.txt && \
    ./install_rest.sh && \
    rm -rf /root/.cache

COPY . /opt/coviddash

RUN echo "/opt/coviddash" > \
    /usr/local/lib/python3.7/dist-packages/coviddash.pth

RUN ln -sf /usr/bin/python3.7 /usr/bin/python
