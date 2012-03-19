from pesquisa_google import GoogleScholarSpider

spider = GoogleScholarSpider()
pagina = spider.run("")
#import ipdb; ipdb.set_trace()
print "Tipo: %s\nResultado: %s" % (type(pagina), str(pagina))
