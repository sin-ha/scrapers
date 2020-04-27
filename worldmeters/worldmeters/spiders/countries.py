# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        countries = response.xpath("//td/a/text()").getall()
        links = response.xpath("//td/a/@href").getall()
        for i in range(len(links)):
            
            
            yield response.follow(url = links[i],callback = self.parse_link , meta = {"id":countries[i]})
            
            
    def parse_link(self,response):
        country = response.request.meta["id"]
        logging.info(country)
        pro = response.xpath("(//tbody)[1]/tr")
        for elements in pro:
            year = elements.xpath(".//td[1]/text()").get()
            population = elements.xpath(".//td[2]/strong/text()").get()
            yield{
                "country":country,
                "year":year,
                "population":population
                }