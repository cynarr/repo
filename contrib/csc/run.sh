SIF_PATH=/projappl/project_2003933/sifs/image_latest.sif \
SNAKEFILE=/opt/coviddash/ingress/workflows/Snakefile \
CLUSC_CONF=`pwd`/clusc.json \
SING_EXTRA_ARGS="--bind `pwd`/clusc.json" \
NUM_JOBS=64 \
NO_CLEANUP=1 \
/projappl/project_2003933/singslurm2/run.sh
