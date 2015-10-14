# coding: utf-8
from __future__ import unicode_literals, print_function

from scrapy.spiders.crawl import CrawlSpider
from scrapy.spiders import Rule

from crawler import settings
from crawler.linkextractors import NextLinkExtractor


class BaseSpider(CrawlSpider):
    name = None
    custom_settings = {}

    def __init__(self, *args, **kwargs):
        self.rules = (
            Rule(NextLinkExtractor(self), callback="handle_page", follow=True),
        )

        _image_store = getattr(settings, "IMAGES_STORE", None)
        _text_store = getattr(settings, "TEXTS_STORE", None)
        if _image_store:
            self.logger.info("The directory of the IMAGE store is %s" % _image_store)
        if _text_store:
            self.logger.info("The directory of the TEXT store is %s" % _text_store)

        spider_site = kwargs.get("site", None)
        if not spider_site:
            spider_site = getattr(settings, "SPIDER_SITE", None)
        self.spider_site = spider_site

        start_urls = getattr(self, "start_urls", None)
        if not start_urls:
            start_urls = getattr(settings, "START_URLS", None)
            if start_urls and self.spider_site:
                start_urls = start_urls[self.name][self.spider_site]
            else:
                start_urls = []
        self.start_urls = start_urls

        allowed_domains = getattr(self, "allowed_domains", None)
        if not allowed_domains:
            allowed_domains = getattr(settings, "ALLOWED_DOMAINS", [])
        self.allowed_domains = allowed_domains

        if self.spider_site:
            css_selector = getattr(self, "css_selector", None)
            if not css_selector:
                css_selector = getattr(settings, "CSS_SELECTORS", {})
                css_selector = css_selector[self.name][self.spider_site]
            self.css_selector = css_selector
        else:
            self.css_selector = {}

        print(self.start_urls, self.css_selector)

        super(BaseSpider, self).__init__(*args, **kwargs)

    def get_css(self, css_name, default=None):
        return self.css_selector.get(css_name, default)

    def handle_page(self, response):
        raise NotImplementedError("This method must be implemented.")

    def parse_start_url(self, response):
        return self.handle_page(response)
