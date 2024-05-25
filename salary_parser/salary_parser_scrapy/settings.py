BOT_NAME = "salary_parser_scrapy"

SPIDER_MODULES = ["salary_parser_scrapy.spiders"]
NEWSPIDER_MODULE = "salary_parser_scrapy.spiders"

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    "salary_parser_scrapy.pipelines.SalaryParserPipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
