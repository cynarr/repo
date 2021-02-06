import os
from urllib.parse import urlsplit
from typing import List
from datetime import datetime
from ingress.mynewsplease import mynewsplease

from newsplease import NewsPlease
from newsplease.crawler.commoncrawl_extractor import CommonCrawlExtractor


all_urls = set()


class UrlFilter(CommonCrawlExtractor):
    def filter_record(self, warc_record, article=None):
        passed_filters, article = super().filter_record(warc_record, article)
        url = warc_record.rec_headers.get_header('WARC-Target-URI')
        if url not in all_urls:
            return False, article
        if article is None:
            article = NewsPlease.from_warc(warc_record)
        return True, article


def main():
    with open(sys.argv[1]) as urls_f:
        for url in urls_f:
            all_urls.add(url.rstrip())
    warc_dir = os.path.join(
        os.environ.get("TMPDIR", "/tmp/"),
        "usenewsfulltexts"
    )
    mynewsplease(
        local_download_dir_warc=warc_dir,
        start_date=datetime(2019, 1, 1),
        end_date=datetime(2020, 12, 31, 23, 59, 59),
        extractor_cls=UrlFilter,
    )


if __name__ == "__main__":
    main()
