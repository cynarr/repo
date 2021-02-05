import sys
import pickle
from os import makedirs
from os.path import join as pjoin
from rpy2 import robjects as ro
from rpy2.robjects import pandas2ri


pandas2ri.activate()

load = ro.r['load']
names = load(sys.argv[1])
outdir = sys.argv[2]
makedirs(outdir, exist_ok=True)

for name in names:
    obj = ro.r[name]
    with open(pjoin(outdir, name + ".pkl"), "wb") as outf:
        pickle.dump(obj, outf)
