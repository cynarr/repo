import os
import sys
import orjson
from loky import cpu_count
import logging
from w3lib.url import canonicalize_url

from newsplease.crawler import commoncrawl_crawler
from newsplease.crawler import commoncrawl_extractor
from multiprocessing import Queue, Pool, Process, active_children
import queue


FINISHED_PRODUCING = object()


LINE_CHUNK_SIZE = 1
MAP_CHUNK_SIZE = 256
QUEUE_SIZE_PER_PROCESS = 16
GET_TIMEOUT = 60 * 60 # 1 hour


def die_all():
    import time
    for child in active_children():
        child.kill()
    time.sleep(5)
    for child in active_children():
        child.terminate()
    sys.exit(-1)


class ChunkingQueue:
    _global_queue = None

    @classmethod
    def init_global_queue(cls, queue_size):
        cls._global_queue = Queue(queue_size)

    def __init__(self, chunk_size, num_producers):
        self._local_queue = []
        self.chunk_size = chunk_size
        self.num_producers = num_producers

    def put(self, item):
        self._local_queue.append(item)
        if len(self._local_queue) == self.chunk_size:
            self._global_queue.put(self._local_queue)
            self._local_queue = []

    def get(self):
        try:
            result = self._global_queue.get(True, GET_TIMEOUT)
        except queue.Empty:
            print("Timeout out waiting for lines", file=sys.stderr)
            die_all()
        return result

    def item_done(self):
        if self._local_queue:
            self._global_queue.put(self._local_queue)
            self._local_queue = []

    def all_producers_done(self):
        self._global_queue.put(FINISHED_PRODUCING)


def quiet_mode():
    from scrapy.utils.log import configure_logging
    configure_logging({"LOG_LEVEL": "ERROR"})
    logging.getLogger('requests').setLevel(logging.CRITICAL)
    logging.getLogger('readability').setLevel(logging.CRITICAL)
    logging.getLogger('PIL').setLevel(logging.CRITICAL)
    logging.getLogger('newspaper').setLevel(logging.CRITICAL)
    logging.getLogger('newsplease').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('jieba').setLevel(logging.CRITICAL)


def get_download_urls(warc_files_start_date):
    cc_news_crawl_names = commoncrawl_crawler.__get_remote_index(warc_files_start_date)
    commoncrawl_crawler.__number_of_warc_files_on_cc = len(cc_news_crawl_names)
    warc_download_urls = []
    for name in cc_news_crawl_names:
        warc_download_url = commoncrawl_crawler.__get_download_url(name)
        warc_download_urls.append(warc_download_url)
    return warc_download_urls


class CommonCrawlProcessor:
    def __init__(
        self,
        callback_on_warc_completed=None,
        valid_hosts=None,
        start_date=None,
        end_date=None,
        warc_files_start_date=None,
        strict_date=True,
        reuse_previously_downloaded_files=True,
        local_download_dir_warc=None,
        continue_after_error=True,
        ignore_unicode_errors=True,
        show_download_progress=False,
        number_of_extraction_processes=4,
        log_level=logging.ERROR,
        delete_warc_after_extraction=True,
        extractor_cls=commoncrawl_extractor.CommonCrawlExtractor,
    ):
        self.queue = ChunkingQueue(
            LINE_CHUNK_SIZE,
            number_of_extraction_processes
        )
        self.valid_hosts = valid_hosts
        self.start_date = start_date
        self.end_date = end_date
        self.warc_files_start_date = warc_files_start_date
        self.strict_date = strict_date
        self.reuse_previously_downloaded_files = reuse_previously_downloaded_files
        self.local_download_dir_warc = local_download_dir_warc
        self.continue_after_error = continue_after_error
        self.ignore_unicode_errors = ignore_unicode_errors
        self.show_download_progress = show_download_progress
        self.number_of_extraction_processes = number_of_extraction_processes
        self.log_level = log_level
        self.delete_warc_after_extraction = delete_warc_after_extraction
        self.extractor_cls = extractor_cls

    def on_valid_article_extracted(self, article):
        article_dict = article.get_dict()
        article_dict["country"] = article.country
        article_dict["canon_url"] = canonicalize_url(article_dict["url"])
        self.queue.put(orjson.dumps(article_dict))

    def callback_on_warc_completed(
        self, warc_path, counter_article_passed, counter_article_discarded,
        counter_article_error, counter_article_total,
    ):
        self.queue.item_done()
        print(
            (
                f"Passed: {counter_article_passed}\t"
                f"Discarded: {counter_article_discarded}\t"
                f"Error: {counter_article_error}\tTotal: {counter_article_total}\t"
            ),
            file=sys.stderr,
            flush=True
        )

    def crawl_urls(self, warc_download_urls):
        quiet_mode()
        with Pool(self.number_of_extraction_processes) as pool:
            for _ in pool.imap_unordered(
                self,
                warc_download_urls,
                chunksize=MAP_CHUNK_SIZE
            ):
                pass
        self.queue.all_producers_done()

    def crawl(self):
        warc_download_urls = get_download_urls(self.warc_files_start_date)
        print("warc_download_urls", file=sys.stderr)
        for warc_url in warc_download_urls:
            print(warc_url, file=sys.stderr)

        process = Process(target=self.crawl_urls, args=(warc_download_urls,))
        process.start()
        self.print_from_queue()
        process.join()

    def print_from_queue(self):
        while 1:
            lines = self.queue.get()
            if lines is FINISHED_PRODUCING:
                return
            else:
                for line in lines:
                    sys.stdout.buffer.write(line)
                    sys.stdout.buffer.write(b"\n")
                sys.stdout.buffer.flush()

    def __call__(self, warc_download_url):
        quiet_mode()
        commoncrawl_extractor = self.extractor_cls()
        commoncrawl_extractor.extract_from_commoncrawl(
            warc_download_url,
            self.on_valid_article_extracted,
            callback_on_warc_completed=self.callback_on_warc_completed,
            valid_hosts=self.valid_hosts,
            start_date=self.start_date, end_date=self.end_date,
            strict_date=self.strict_date,
            reuse_previously_downloaded_files=self.reuse_previously_downloaded_files,
            local_download_dir_warc=self.local_download_dir_warc,
            continue_after_error=self.continue_after_error,
            ignore_unicode_errors=self.ignore_unicode_errors,
            show_download_progress=self.show_download_progress,
            log_level=self.log_level,
            delete_warc_after_extraction=self.delete_warc_after_extraction
        )


def default_cpus():
    if "NEWS_PLEASE_WORKERS" in os.environ:
        return int(os.environ["NEWS_PLEASE_WORKERS"])
    else:
        return cpu_count()


def mynewsplease(**kwargs):
    kwargs["warc_files_start_date"] = kwargs.get("warc_files_start_date", kwargs.get("start_date"))
    number_of_extraction_processes = kwargs.pop(
        "number_of_extraction_processes",
        default_cpus()
    )
    ChunkingQueue.init_global_queue(number_of_extraction_processes * QUEUE_SIZE_PER_PROCESS)
    ignore_unicode_errors = kwargs.pop(
        "ignore_unicode_errors",
        True
    )
    quiet_mode()
    CommonCrawlProcessor(
        number_of_extraction_processes=number_of_extraction_processes,
        ignore_unicode_errors=ignore_unicode_errors,
        **kwargs
    ).crawl()
