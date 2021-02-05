import os
from urllib.parse import urlsplit
from typing import List
from datetime import datetime
from newsplease import NewsPlease

from newsplease.crawler.commoncrawl_extractor import CommonCrawlExtractor


class BertPreproc:
    def __init__(self):
        from tokenizers import Tokenizer
        from tokenizers.pre_tokenizers import BertPreTokenizer
        from tokenizers.normalizers import BertNormalizer
        from tokenizers.models import WordLevel

        self.tokenizer = Tokenizer(WordLevel({"UNK": 0}, "UNK"))
        self.tokenizer.pre_tokenizer = BertPreTokenizer()
        self.tokenizer.normalizer = BertNormalizer()

    def __call__(self, inp: str) -> List[str]:
        return self.tokenizer.encode(inp)


preproc = BertPreproc()


class KeywordFilterCommonCrawl(CommonCrawlExtractor):
    def filter_record(self, warc_record, article=None):
        passed_filters, article = super().filter_record(warc_record, article)
        if not passed_filters:
            return False, article
        url = warc_record.rec_headers.get_header('WARC-Target-URI')
        netloc = urlsplit(url).netloc
        # TLD filtering XXX: stub
        if netloc.strip(".").rsplit(".", 1)[-1] not in ("fi", "ee", "uk", "ie", "es", "fr", "de", "se"):
            return False, article
        # We definitely need the full article object now
        if article is None:
            article = NewsPlease.from_warc(warc_record)
        # Filter by language XXX: stub
        if article.language not in ("fi", "et", "en", "es", "fr", "de", "sv"):
            return
        # Keywords XXX: stub
        bits = article.text
        if "korona" not in bits and "covid" not in bits:
            return False, article
        return True, article


def main():
    from ingress.mynewsplease import newsplease
    warc_dir = os.path.join(
        os.environ.get("TMPDIR", "/tmp/"),
        "newscrawlcovid202003"
    )
    newsplease(
        local_download_dir_warc=warc_dir,
        start_date=datetime(2020, 3, 1),
        end_date=datetime(2020, 3, 31, 23, 59, 59),
        extractor_cls=KeywordFilterCommonCrawl,
    )


if __name__ == "__main__":
    main()
