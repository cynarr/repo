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

REMOVE_PREFIX = "statistics.actual."

MEDIACLOUD_KEEP = [
    "title",
    "url"
]

CROWDTANGLE_NAMES = ["crowdtangle2019", "crowdtangle2020"]
MEDIACLOUD_NAMES = ["mediacloud2019", "mediacloud2020"]

for name in names:
    obj = ro.r[name]
    if name in CROWDTANGLE_NAMES:
        keep_cols = CROWDTANGLE_KEEP
        if name == "crowdtangle2019":
            keep_cols.remove("statistics.actual.careCount")
    elif name in MEDIACLOUD_NAMES:
        keep_cols = MEDIACLOUD_KEEP
    else:
        continue
    obj.drop(obj.columns.difference(keep_cols), 1, inplace=True)
    type_map = {
        col: str if col in ["title", "url", "link"] else int
        for col
        in keep_cols
    }
    obj = obj.astype(type_map, copy=False)
    obj.rename(
        lambda col_name:
            col_name[len(REMOVE_PREFIX):]
            if col_name.startswith(REMOVE_PREFIX)
            else col_name
    )
    # obj.fillna(0, inplace=True)
    table = pyarrow.Table.from_pandas(obj)
    with pyarrow.OSFile(pjoin(outdir, name + ".arrow"), 'wb') as sink:
        with pyarrow.RecordBatchFileWriter(sink, table.schema) as writer:
            writer.write_table(table)
