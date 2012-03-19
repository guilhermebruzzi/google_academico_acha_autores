# -- coding: UTF-8 --

import ast
import os
import urllib
from propriedades import propriedades
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item, Field
from scrapy.spider import BaseSpider
from scrapy.http import Request
        
class GoogleScholarItem(Item):
    url = Field()
    citation_title = Field()
    citation_author = Field()
    citation_authors = Field()
    citation_date = Field()
    citation_publisher = Field()
    
class GoogleScholarSpider(BaseSpider):

    name = 'GoogleScholar'
    allowed_domains = ['scholar.google.com.br']
    dict_file = os.path.abspath(os.path.dirname(__file__)) + "/googlescholar.json"

    def parse(self, response):
        return Request("http://www.example.com/some_page.html",
                      callback=self.parse_page2)

    def parse_page_searched(self, response):
        x = HtmlXPathSelector(response)

        item = GoogleScholarItem()
        item['url'] = response.url
        for propriedade in propriedades:
            item[propriedade] = x.select("//meta[@name='" + propriedade + "']/@content").extract()
        open(self.dict_file, 'wb').write(str(item))
        return item

    def __get_dict_from_file__(self):
        json = open(self.dict_file, 'r').readlines()
        json = "".join(json)
        json = json.replace("\n", "")
        return ast.literal_eval(json) #Retorna o dicionário em si

    def run(self, pesquisa):
        url = 'http://scholar.google.com.br/scholar?hl=pt-BR&' + urllib.urlencode({"q": pesquisa})
        return Request("http://dl.acm.org/citation.cfm?id=1721672", callback=self.parse_page_searched)

