# -- coding: UTF-8 --

import hashlib
import os
import tornado
from tornado.web import Application, RequestHandler, HTTPError, StaticFileHandler
from propriedades import propriedades
from pesquisa_google import GoogleScholarSpider
from template import render_template

class PesquisaHandler(tornado.web.RequestHandler):

    def __get_pdfs_separadamente__(self, urls):
        urls_nao_pdf = []
        urls_pdf = []
        for url in urls:
            url_md5 = hashlib.md5(url).hexdigest()
            if url.endswith(".pdf"):
                urls_pdf.append({"md5": url_md5,"val": url})
            else:
                urls_nao_pdf.append({"md5": url_md5,"val": url})
                
        return (urls_nao_pdf, urls_pdf)

    def __call_template_pesquisa__(self, pesquisa=None, urls=None):
        title = "Pesquisa no Google Acadêmico" if pesquisa == None else "Resultado da pesquisa: " + pesquisa
        if urls != None:
            urls, urls_pdf = self.__get_pdfs_separadamente__(urls)
        options = {"title": title, "urls": urls, "urls_pdf": urls_pdf}
        result = render_template("templates/pesquisa.html", options)
        self.write(result)

    def get(self):
        """ Quando a página google_academico_acha_autores/?pesquisa=texto carregar """
        try:
            pesquisa = self.get_argument("pesquisa")
        except:
            pesquisa = None
            urls = None
        if pesquisa != None:
            spider = GoogleScholarSpider()
            spider.run_google_search(pesquisa)
            urls = spider.get_dict_urls()["urls"]
        self.__call_template_pesquisa__(pesquisa, urls)

class GetPageHandler(tornado.web.RequestHandler):

    def __format_resultado__(self, resultado):
        resultado_formatado = []
        resultado["citation_authors"] = resultado["citation_authors"] + resultado["citation_author"]
        del(resultado["citation_author"])

        for propriedade in propriedades:
            if resultado.has_key(propriedade):
                propriedade_valor = {"label": propriedade.replace("_", " "), "valor": ""}
                for valor in resultado[propriedade]:
                    propriedade_valor["valor"] += " " + valor
                propriedade_valor["valor"] = propriedade_valor["valor"].strip()
                resultado_formatado.append(propriedade_valor)

        return resultado_formatado

    def __call_template_propriedades__(self, resultado):
        options = {"resultado": resultado}
        result = render_template("templates/propriedades.html", options)
        self.write(result)

    def get(self, url):
        spider = GoogleScholarSpider()
        spider.run_page_parser(url)
        resultado = spider.get_dict_authors()
        resultado = self.__format_resultado__(resultado)
        self.__call_template_propriedades__(resultado)

STATIC_PATH = os.path.abspath(os.path.dirname(__file__))
routes_google_academico_acha_autores = [
    (r"/google_academico_acha_autores/css/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/css/"}),
    (r"/google_academico_acha_autores/js/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/js/"}),
    (r"/google_academico_acha_autores/img/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/img/"}),
    (r"/google_academico_acha_autores/get_page/(.*)", GetPageHandler),
    (r"/google_academico_acha_autores/?.*", PesquisaHandler)
]
