[![Docker Repository on Quay](https://quay.io/repository/mood-mapping-muppets/repo/status "Docker Repository on Quay")](https://quay.io/repository/mood-mapping-muppets/repo)

# Covid-dash

COVID-19 European news text analysis dashboard for the Embeddia hackathon.

## Ingress + analysis pipeline

### Manual setup

Get [Poetry](https://python-poetry.org/):

  $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Install:

  $ ./install.sh

### Docker/Singularity

Containers use [GitHub Container
Registry](https://github.com/orgs/mood-mapping-muppets/packages?ecosystem=container).

Pull with Docker:

  $ docker pull ghcr.io/mood-mapping-muppets/image:latest

Pull with Singularity:

  $ singularity pull docker://ghcr.io/mood-mapping-muppets/image:latest

### Running ingress

Manually you can run:

  $ cd ingress
  $ poetry run snakemake get_covid_march

On CSC you copy the files in `contrib/csc` into a working directory and modify
the paths as necessary and then run:

  $ ./run.sh

## Dashboard

### Manual setup

TODO

### Docker

TODO

### Deploying to Rahti

TODO
