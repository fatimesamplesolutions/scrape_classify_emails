# -*- coding: utf-8 -*-
import re

import scrapy
from twisted.python import failure

from scrape_emails.items import ScrapeEmailsItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

import pandas as pd


class ScrapeEmailSpider(scrapy.Spider):
    name = 'scrape_email'
    # allowed_domains = ['urls.csv']
    # start_urls = ['http://urls.csv/']

    f = open("urls_to_scrape_full_urls.csv")
    start_urls = [url.strip() for url in f.readlines()]
    allowed_domains = [start_urls]
    f.close()

    handle_httpstatufs_list = range(200, 600)
    # handle_httpstatus_all=True

    bad_log_file = 'b.csv'

    found_url = 'found_url.csv'
    not_found_url = 'not_found_url.csv'
    redirected_urls = 'redirected_urls.csv'
    internal_server_error = 'internal_err.csv'

    def parse(self, response):

        if response:
            selector = response.xpath('//body//*[not(self::script) and not(self::style)]').extract()
            sanitized = ''.join([re.sub(r'^\s+', '', item) for item in selector])
            pattern = re.compile('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
            emails = pattern.findall(sanitized)
            v = set(emails)

            emailitems = []

            for email in zip(v): # used zip function because it returns an iterator
                emailitem = ScrapeEmailsItem()
                emailitem['email'] = email
                emailitem['url'] = response.url
                emailitems.append(emailitem)
                return emailitems

        self.handle_status_codes(response)

    def handle_status_codes(self, response):

        if response.status == 200:
            self.append(self.found_url, response.url)

        elif response.status == 301 or response.status == 302 or response.status == 303 or response.status == 307:
            self.append(self.redirected_urls, response.url)

        elif response.status == 404 or response.status == 403:
            self.append(self.not_found_url, response.url)

        elif response.status == 500 or response.status == 503:
            self.append(self.internal_server_error, response.url)

        elif response.status == DNSLookupError:
            self.append(self.bad_log_file, response.url)

        else:
            self.append(self.bad_log_file, response.url)


    def append(self, file, string):
        file = open(file, 'a')
        file.write(string + "\n")
        file.close()