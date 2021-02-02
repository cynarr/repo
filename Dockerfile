FROM python:3.9.1-slim-buster

RUN apt-get install -y zstd

RUN python3 -m pip install --upgrade \
    pip==20.2.4 \
    setuptools==50.3.2 \
    poetry==1.1.4

WORKDIR /opt/coviddash

COPY pyproject.toml poetry.lock ./

RUN poetry export \
      --without-hashes | \
    python3 -m pip install -r requirements.txt && \
    rm requirements.txt &&
    ./install_rest.sh && \
    rm -rf /root/.cache

COPY . /opt/coviddash

RUN echo "/opt/coviddash" > \
    /usr/local/lib/python3.9/dist-packages/coviddash.pth
