#!/bin/bash

PRE_SCRIPT=$(cat <<'END_PRE_SCRIPT'
# From CSC singularity_wrapper
CSC_SING_FLAGS="-B /users:/users -B /projappl:/projappl -B /scratch:/scratch -B /appl/data:/appl/data"
if [ -n "$TMPDIR" ]; then
    CSC_SING_FLAGS="$SING_FLAGS -B $TMPDIR:$TMPDIR"
fi
if [ -n "$LOCAL_SCRATCH" ]; then
    CSC_SING_FLAGS="$SING_FLAGS -B $LOCAL_SCRATCH:$LOCAL_SCRATCH"
fi
SING_EXTRA_ARGS="$CSC_SING_FLAGS $SING_EXTRA_ARGS"
END_PRE_SCRIPT
)

PRE_SCRIPT="$PRE_SCRIPT" \
SIF_PATH=/projappl/project_2003933/sifs/pipe_latest.sif \
SNAKEFILE=/opt/coviddash/ingress/workflow/Snakefile \
CLUSC_CONF=`pwd`/clusc.json \
SING_EXTRA_ARGS="--bind `pwd`/clusc.json" \
NUM_JOBS=64 \
NO_CLEANUP=1 \
TRACE=1 \
OVERRIDE_TMPDIR=/scratch/project_2003933/tmp/ \
/projappl/project_2003933/singslurm2/run.sh all
