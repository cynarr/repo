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

On CSC you first need to get [singslurm2](https://github.com/frankier/singslurm2):

    $ cd /projappl/project_2003933
    $ git clone --recursive https://github.com/frankier/singslurm2.git

You can then copy the files in `contrib/csc` into a working directory and
modify the paths as necessary and then run:

    $ nohup ./run.sh &

Note you CWD must not contain any symlinks when running Singularity. To be safe
you should run e.g. `cd $(realpath .)` first.

## Dashboard

### Manual setup

TODO

### Docker

TODO

### Deploying to Rahti

TODO
