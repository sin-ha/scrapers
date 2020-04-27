# -*- coding: utf-8 -*-
import scrapy
import logging

class CountryscraperSpider(scrapy.Spider):
    name = 'countryScraper'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        items = response.xpath('(//table[@id="main_table_countries_today"]/tbody)[1]/tr[@style=""]')
        for item in items:
            link = item.xpath('.//td/a/@href').get()
            name = item.xpath('.//td/a/text()').get()
            if(link):
                yield response.follow(url=link, callback=self.parse_link, meta={"id": name})
            else:
                yield {
                    "country": name,
                    "total_cases" :None,
                    "cases_having_results" : None,
                    "dead" : None,
                    "cured": None
                }
    def parse_link(self,response):
        name = response.request.meta["id"]
        logging.info(name)
        counters = response.xpath('//div[@class="maincounter-number"]/span/text()').getall()
        total = counters[0]
        living = counters[1]
        dead = counters[2]
        s = living.replace(',', '')
        d = dead.replace(',', '')
        try:
            results = str(int(s)+int(d))
        except:
            results = None
        yield {
        "country" : name,
        "total_cases" :total,
        "cases_having_results" : results,
        "dead" : dead,
        "cured": living
        }
