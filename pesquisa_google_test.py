# -- coding: UTF-8 --

import unittest
from pesquisa_google import GoogleScholarSpider

#spider = GoogleScholarSpider()
#pagina = spider.run("")
#print "Tipo: %s\nResultado: %s" % (type(pagina), str(pagina))

class GoogleScholarSpiderTest(unittest.TestCase):
    
    def setUp(self):
        self.spider = GoogleScholarSpider()
    
    def get_first_10_urls(self):
        resultado = self.spider.get_dict_urls()
        assert 'http://dl.acm.org/citation.cfm?id=1721672' in resultado["url"]
        self.assertEquals(len(resultado["url"]), 10)
        
    def get_some_authors(self):
        resultado = self.spider.get_dict_authors()
        assert 'Armbrust, Michael' in resultado[0]["citation_authors"][0]
        assert 'Katz, Randy' in resultado[0]["citation_authors"][0]
    
    def run_test(self):
        self.spider.run_google_search("cloud computing")
        self.get_first_10_urls()
        self.spider.run_pages_parser()
        self.get_some_authors()

