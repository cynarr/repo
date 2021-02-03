FROM quay.io/bitnami/python:3.8.7-prod

RUN apt-get update && \
    apt-get install -y zstd && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade \
    pip==20.2.4 \
    setuptools==50.3.2 \
    poetry==1.1.4

WORKDIR /opt/coviddash

COPY pyproject.toml poetry.lock ./

RUN poetry export \
      --without-hashes | \
    python3 -m pip install -r requirements.txt && \
    rm requirements.txt && \
    ./install_rest.sh && \
    rm -rf /root/.cache

COPY . /opt/coviddash

RUN echo "/opt/coviddash" > \
    /usr/local/lib/python3.9/dist-packages/coviddash.pth
