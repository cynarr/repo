import os
from urllib.parse import urlsplit
from typing import List
from datetime import datetime
from ingress.mynewsplease import mynewsplease

from newsplease import NewsPlease
from newsplease.crawler.commoncrawl_extractor import CommonCrawlExtractor
from mmmbgknow.country_detect import detect_country
from mmmbgknow.european import is_european_cc, is_european_langcode



class BertPreproc:
    def __init__(self):
        from tokenizers import Tokenizer
        from tokenizers.pre_tokenizers import BertPreTokenizer
        from tokenizers.normalizers import BertNormalizer
        from tokenizers.models import WordLevel

        self.tokenizer = Tokenizer(WordLevel({"UNK": 0}, unk_token="UNK"))
        self.tokenizer.pre_tokenizer = BertPreTokenizer()
        self.tokenizer.normalizer = BertNormalizer()

    def __call__(self, inp: str) -> List[str]:
        return self.tokenizer.encode(inp).tokens


preproc = BertPreproc()


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
