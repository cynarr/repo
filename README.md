# Covid-dash

COVID-19 European news text analysis dashboard for the Embeddia hackathon.

## Ingress + analysis pipeline

### Manual setup

Get [Poetry](https://python-poetry.org/):

    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

Or in Powershell:

    $ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

Install:

    $ ./install.sh

If you want to run the usenews extraction you also need to install R, including
development packages (`r-base` and `r-base-dev` on Debian-oids) and the usenews
extra:

    $ ./install.sh -E usenews

### Docker/Singularity

Containers use [GitHub Container
Registry](https://github.com/orgs/mood-mapping-muppets/packages?ecosystem=container).

Pull with Docker:

    $ docker pull ghcr.io/mood-mapping-muppets/pipe:latest

Pull with Singularity:

    $ singularity pull docker://ghcr.io/mood-mapping-muppets/pipe:latest

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

### Manual setup and run

Get Poetry as above.

Change directory and install.

    $ cd dashboard
    $ poetry install

Now you can run:

    $ poetry run python app.py

### Docker

You can run the production `Dockerfile` locally.

    $ docker run ghcr.io/mood-mapping-muppets/web:latest

### Deploying to Rahti

The container is automatically deployed through GitHub actions.
