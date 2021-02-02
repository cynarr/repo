import hashlib
import os
import sys
import orjson
from loky import cpu_count

from newsplease.crawler import commoncrawl_crawler as commoncrawl_crawler


def on_valid_article_extracted(article):
    """
    This function will be invoked for each article that was extracted
    successfully from the archived data and that satisfies the filter criteria.

    :param article:
    :return:
    """
    sys.stdout.buffer.write(orjson.dumps(article.get_dict()))


def callback_on_warc_completed(
    warc_path, counter_article_passed, counter_article_discarded,
    counter_article_error, counter_article_total, counter_warc_processed
):
    """
    This function will be invoked for each WARC file that was processed
    completely. Parameters represent total values, i.e., accumulated over all
    all previously processed WARC files.

    :param warc_path:
    :param counter_article_passed:
    :param counter_article_discarded:
    :param counter_article_error:
    :param counter_article_total:
    :param counter_warc_processed:
    :return:
    """
    sys.stderr.write(
        f"Passed: {counter_article_passed}\t"
        f"Discarded: {counter_article_discarded}\t"
        f"Error: {counter_article_error}\tTotal: {counter_article_total}\t"
        f"WARCs processed: {counter_warc_processed}"
    )


def newsplease(**kwargs):
    number_of_extraction_processes = kwargs.pop("number_of_extraction_processes", cpu_count())
    commoncrawl_crawler.crawl_from_commoncrawl(
        on_valid_article_extracted,
        callback_on_warc_completed=callback_on_warc_completed,
        continue_process=True,
        number_of_extraction_processes=number_of_extraction_processes,
        **kwargs
    )
