# -- coding: UTF-8 --

import ast
import hashlib
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
    
class GoogleScholarLink(Item):
    urls = Field()
    
class GoogleScholarSpider(BaseSpider):

    name = 'GoogleScholar'
    allowed_domains = ['scholar.google.com.br']
    main_url = os.environ['url'] if os.environ.has_key('url') else ""
    start_urls = [main_url]
    dict_urls_file = os.path.abspath(os.path.dirname(__file__)) + "/data/urls.json"
    dict_authors_file = "" # Será alterado dinamicamente
    
    def __parse_google_search__(self, response):
        x = HtmlXPathSelector(response)
        link = GoogleScholarLink()
        link['urls'] = x.select("//h3[@class='gs_rt']/a/@href").extract()
        open(self.dict_urls_file, 'wb').write(str(link))
        return link
        
    def __set_dict_authors_file__(self, url):
        url_md5 = hashlib.md5(url).hexdigest()
        self.dict_authors_file = os.path.abspath(os.path.dirname(__file__)) + "/data/" + url_md5 + ".json"
        
    def __parse_page_found__(self, response):
        x = HtmlXPathSelector(response)

        item = GoogleScholarItem()
        item['url'] = response.url
        self.__set_dict_authors_file__(self.main_url.strip())
        for propriedade in propriedades:
            if propriedade != "url":
                item[propriedade] = x.select("//meta[@name='" + propriedade + "']/@content").extract()
        open(self.dict_authors_file, 'w').write(str(item))
        return item
        
    def parse(self, response):
        if self.main_url.startswith("http://scholar.google.com.br"):
            return self.__parse_google_search__(response)
        else:
            return self.__parse_page_found__(response)

    def __get_dict_from_file__(self, dict_file):
        json = open(dict_file, 'r').readlines()
        json = "".join(json)
        json = json.replace("\n", "")
        return ast.literal_eval(json) #Retorna o dicionário em si
        
    def get_dict_urls(self):
        return self.__get_dict_from_file__(self.dict_urls_file)
        
    def get_dict_authors(self):
        return self.__get_dict_from_file__(self.dict_authors_file)

    def __call_spider_on_url__(self, url):
        arquivo_spider = __file__.replace(".pyc", ".py")
        cmd = 'url="%s" scrapy runspider %s' % (url.strip(), arquivo_spider)
        os.system(cmd)
    
    def run_page_parser(self, url):
        self.__set_dict_authors_file__(url)
        self.__call_spider_on_url__(url)

    def run_google_search(self, pesquisa):
        url = 'http://scholar.google.com.br/scholar?hl=pt-BR&' + urllib.urlencode({"q": pesquisa})
        self.__call_spider_on_url__(url)

