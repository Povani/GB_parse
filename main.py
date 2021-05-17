from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from GB_parse.avito_parse.spiders.avito_parsing import AvitoParsingSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule('avito_parse.settings')
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AvitoParsingSpider)
    crawler_process.start()
