from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from GB_parse.hh.spiders import HH


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("GB_parse.hh.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(HH)
    crawler_process.start()
