# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
import re


# from scrapy.contrib.spidermiddleware.httperror import HttpError
from scrape_emails.items import ScrapeEmailsItem


class TestSpider(scrapy.Spider):
    name = "scrp_emails"

    f = open("urls_to_scrape_full_urls.csv")
    start_urls = [url.strip() for url in f.readlines()]
    allowed_domains = [start_urls]
    f.close()

    bad_log_file = 'bad_url.csv'

    found_url = 'found_url_2.csv'
    not_found_url = 'not_found_url_2.csv'
    redirected_urls = 'redirected_urls_2.csv'
    internal_server_error = 'internal_err_2.csv'

    dns_error = 'dns_error.csv'
    timeout_error = 'timeout.csv'

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse_httpbin, errback=self.errback_httpbin, dont_filter=True)


    def parse_httpbin(self, response):

        self.handle_status_codes(response)

        selector = response.xpath('//body//*[not(self::script) and not(self::style)]').extract()
        sanitized = ''.join([re.sub(r'^\s+', '', item) for item in selector])
        pattern = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
        emails = pattern.findall(sanitized)
        v = set(emails)

        emailitems = []

        for email in zip(v):
            emailitem = ScrapeEmailsItem()
            emailitem['email'] = email
            emailitem['url'] = response.url
            emailitems.append(emailitem)
            return emailitems


    def handle_status_codes(self, response):

        if response.status in range(200, 299) :
            self.append(self.found_url, response.url)

        elif response.status in range(300, 399):
            self.append(self.redirected_urls, response.url)

        elif response.status == 404:
            self.append(self.not_found_url, response.url)

        elif response.status in range(400, 499):
            self.append(self.not_found_url, response.url)

        elif response.status in range(500, 599):
            self.append(self.internal_server_error, response.url)

        else:
            self.append(self.bad_log_file, response.url)


    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            # self.logger.error('HttpError on %s', response.url)
            self.append(self.bad_log_file, response.url)

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            # self.logger.error('DNSLookupError on %s', request.url)
            self.append(self.dns_error, request.url)

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            # self.logger.error('TimeoutError on %s', request.url)
            self.append(self.dns_error, request.url)

        else:
            self.append(self.bad_log_file, failure.request.url)

    def append(self, file, string):
        file = open(file, 'a')
        file.write(string + "\n")
        file.close()