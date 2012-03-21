# -- coding: UTF-8 --

import os
import tornado
from tornado.web import Application, RequestHandler, HTTPError, StaticFileHandler
from propriedades import propriedades
from pesquisa_google import GoogleScholarSpider
from template import render_template

class PesquisaHandler(tornado.web.RequestHandler):

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
        
    def __get_resultados__(self, spider):
        resultados = spider.get_dict_authors()
        resultados_formatados = []
        for resultado in resultados:
            resultado = self.__format_resultado__(resultado)
            resultados_formatados.append(resultado)
        return resultados_formatados

    def __call_template_pesquisa__(self, pesquisa=None, resultados=None):
        title = "Pesquisa no Google Acadêmico" if pesquisa == None else "Resultado da pesquisa: " + pesquisa
        options = {"title": title, "resultados": resultados}
        result = render_template("pesquisa.html", options)
        self.write(result)

    def get(self):
        """ Quando a página google_academico_acha_autores/?pesquisa=texto carregar """
        try:
            pesquisa = self.get_argument("pesquisa")
        except:
            pesquisa = None
            resultados = None
        if pesquisa != None:
            spider = GoogleScholarSpider()
            spider.run_google_search(pesquisa)
            spider.run_pages_parser()
            resultados = self.__get_resultados__(spider)
        self.__call_template_pesquisa__(pesquisa, resultados)
            
        
STATIC_PATH = os.path.abspath(os.path.dirname(__file__))
routes_google_academico_acha_autores = [
    (r"/google_academico_acha_autores/css/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/css/"}),
    (r"/google_academico_acha_autores/js/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/js/"}),
    (r"/google_academico_acha_autores/img/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/img/"}),
    (r"/google_academico_acha_autores/?.*", PesquisaHandler)
]
