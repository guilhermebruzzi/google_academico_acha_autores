# -- coding: UTF-8 --

import unittest
from pesquisa_google import GoogleScholarSpider

class GoogleScholarSpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = GoogleScholarSpider()
        self.search_test = 'cloud computing'
        self.url_test = 'http://dl.acm.org/citation.cfm?id=1721672'
        self.author_test = 'Katz, Randy'
        self.url_test2 = 'http://www.mendeley.com/research/gartner-seven-cloudcomputing-security-risks-4/'
        self.author_test2 = 'Cloud, Network World'
    
    def run_google_search_test(self):
        self.spider.run_google_search(self.search_test)
        urls = self.spider.get_dict_urls()["urls"]
        assert self.url_test in urls
        self.assertEquals(len(urls), 10)
        
    def run_page_parser_test(self):
        self.spider.run_page_parser(self.url_test)
        authors = self.spider.get_dict_authors()["citation_authors"][0]
        self.spider.run_page_parser(self.url_test2)
        authors2 = self.spider.get_dict_authors()["citation_authors"][0]
        
        assert self.author_test in authors
        assert self.author_test2 in authors2

