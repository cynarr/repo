import sys
from os import makedirs
from os.path import join as pjoin
from rpy2 import robjects as ro
from rpy2.robjects import pandas2ri
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

CROWDTANGLE_NAMES = ["crowdtangle2019", "crowdtangle2020"]
MEDIACLOUD_NAMES = ["mediacloud2019", "mediacloud2020"]

for name in names:
    obj = ro.r[name]
    if name in CROWDTANGLE_NAMES:
        keep_cols = CROWDTANGLE_KEEP
    elif name in MEDIACLOUD_NAMES:
        keep_cols = MEDIACLOUD_KEEP
    else:
        continue
    obj.drop(obj.columns.difference(keep_cols), 1, inplace=True)
    obj.fillna(0, inplace=True)
    table = pyarrow.Table.from_pandas(obj)
    with pyarrow.OSFile(pjoin(outdir, name + ".arrow"), 'wb') as sink:
        with pyarrow.RecordBatchFileWriter(sink, table.schema) as writer:
            writer.write_table(table)
