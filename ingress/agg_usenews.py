from os.path import join as pjoin
import sys
import pyarrow
import pandas
from mmmbgknow.url import urlnorm


usenews_arrows = sys.argv[1]
tables_files = {
    "mediacloud": [
        pjoin(usenews_arrows, "mediacloud2019.arrow"),
        pjoin(usenews_arrows, "mediacloud2020.arrow"),
    ],
    "crowdtangle": [
        pjoin(usenews_arrows, "crowdtangle2019.arrow"),
        pjoin(usenews_arrows, "crowdtangle2020.arrow"),
    ]
}
tables = {}

for name, files in tables_files.items():
    sub_tables = []
    for file in files:
        source = pyarrow.memory_map(file, 'r')
        sub_tables.append(pyarrow.ipc.RecordBatchFileReader(source).read_all())
    tables[name] = pyarrow.concat_tables(sub_tables)

tables["crowdtangle"]["link"].map(urlnorm)
tables["mediacloud"]["guid"].map(urlnorm)

joined = pandas.merge(
    tables["crowdtangle"].groupby(["link"]).sum(),
    tables["mediacloud"],
    left_on="link",
    right_on="guid",
)

with pyarrow.OSFile(sys.argv[2], 'wb') as sink:
    with pyarrow.RecordBatchFileWriter(sink, joined.schema) as writer:
        writer.write_table(joined)
