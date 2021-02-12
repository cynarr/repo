import sys
import pickle
from os import makedirs
from os.path import join as pjoin
from rpy2 import robjects as ro
from rpy2.robjects import pandas2ri
from pandas import DataFrame
import pyarrow


pandas2ri.activate()

load = ro.r['load']
names = load(sys.argv[1])
outdir = sys.argv[2]
makedirs(outdir, exist_ok=True)

CROWDTANGLE_KEEP = [
    "link",
    "statistics.actual.likeCount",
    "statistics.actual.shareCount",
    "statistics.actual.commentCount",
    "statistics.actual.loveCount",
    "statistics.actual.wowCount",
    "statistics.actual.hahaCount",
    "statistics.actual.sadCount",
    "statistics.actual.angryCount",
    "statistics.actual.thankfulCount",
    "statistics.actual.careCount",
]

MEDIACLOUD_KEEP = [
    "title"
    "guid"
]

for name in names:
    obj = ro.r[name]
    if name.startswith("mediacloud."):
        keep_cols = MEDIACLOUD_KEEP
    elif name.startswith("crowdtangle"):
        keep_cols = CROWDTANGLE_KEEP
    else:
        continue
    obj.drop(obj.columns.difference(keep_cols), 1, inplace=True)
    obj.fillna(0, inplace=True)
    with pyarrow.OSFile(pjoin(outdir, name + ".arrow"), 'wb') as sink:
        with pyarrow.RecordBatchFileWriter(sink, obj.schema) as writer:
            writer.write_table(obj)
