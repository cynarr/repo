import os
from datetime import datetime
from ingress.mynewsplease import mynewsplease

from newsplease import NewsPlease
from newsplease.crawler.commoncrawl_extractor import CommonCrawlExtractor
from mmmbgknow.european import is_european_langcode
from mmmbgknow.state_broadcaster import STATE_BROADCASTERS
from ingress.search_utils import get_covid_searchers
import tldextract


class StateBroadcasterKeywordFilterCommonCrawl(CommonCrawlExtractor):
    def filter_record(self, warc_record, article=None):
        url = warc_record.rec_headers.get_header('WARC-Target-URI')
        url_parts = tldextract.extract(url)
        domain = url_parts.registered_domain
        if domain not in STATE_BROADCASTERS:
            return False, article
        country = STATE_BROADCASTERS[domain]

        passed_filters, article = super().filter_record(warc_record, article)

        if not passed_filters:
            return False, article
        if article is None:
            article = NewsPlease.from_warc(warc_record)
        article.country = country
        if not article.language or not is_european_langcode(article.language):
            return False, article
        searcher = get_covid_searchers().get(article.language)
        if searcher is None:
            return False, article

        def match(key):
            return searcher.match(
                (getattr(article, key) or "").lower().encode("utf-8")
            )
        if not match("title") and not match("maintext"):
            return False, article
        return True, article


def main():
    warc_dir = os.path.join(
        os.environ.get("TMPDIR", "/tmp/"),
        "newscrawlstatebroadcastercovid"
    )
    mynewsplease(
        local_download_dir_warc=warc_dir,
        start_date=datetime(2020, 1, 1),
        extractor_cls=StateBroadcasterKeywordFilterCommonCrawl,
    )


if __name__ == "__main__":
    main()
