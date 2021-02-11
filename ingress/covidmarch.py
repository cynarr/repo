import os
from datetime import datetime
from ingress.mynewsplease import mynewsplease

from newsplease import NewsPlease
from newsplease.crawler.commoncrawl_extractor import CommonCrawlExtractor
from mmmbgknow.country_detect import detect_country
from mmmbgknow.european import is_european_cc, is_european_langcode
from mmmbgknow.pickled_searchers import get_covid


_covid_searchers = None


def get_covid_searchers():
    global _covid_searchers
    if _covid_searchers is None:
        _covid_searchers = get_covid()
    return _covid_searchers


class KeywordFilterCommonCrawl(CommonCrawlExtractor):
    def filter_record(self, warc_record, article=None):
        passed_filters, article = super().filter_record(warc_record, article)
        if not passed_filters:
            return False, article
        url = warc_record.rec_headers.get_header('WARC-Target-URI')

        def get_lang():
            nonlocal article
            if article is None:
                article = NewsPlease.from_warc(warc_record)
            return article.language
        country = detect_country(url, get_lang)
        if not country or not is_european_cc(country):
            return False, article
        article.country = country
        if article is None:
            article = NewsPlease.from_warc(warc_record)
        lang = article.language
        if not lang or not is_european_langcode(lang):
            return False, article
        # TODO: Find COVID-19 mention
        searcher = get_covid_searchers().get(lang)
        if searcher is None:
            return False, article

        def match(key):
            return searcher.match(
                (getattr(article, key) or "").lower().encode("utf-8")
            )
        if match("title"):
            return True, article
        if match("maintext"):
            return True, article
        return True, article


def main():
    warc_dir = os.path.join(
        os.environ.get("TMPDIR", "/tmp/"),
        "newscrawlcovid202003"
    )
    mynewsplease(
        local_download_dir_warc=warc_dir,
        start_date=datetime(2020, 3, 1),
        end_date=datetime(2020, 3, 31, 23, 59, 59),
        extractor_cls=KeywordFilterCommonCrawl,
    )


if __name__ == "__main__":
    main()
