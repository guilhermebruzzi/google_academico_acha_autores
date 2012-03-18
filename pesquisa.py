# -- coding: UTF-8 --

import os
import tornado
from tornado.web import Application, RequestHandler, HTTPError, StaticFileHandler
from template import render_template

class PesquisaHandler(tornado.web.RequestHandler):
    
    def get_resultado(self, pesquisa):
        return None
    
    def call_template_pesquisa(self, pesquisa=None, resultado=None):
        title = "Pesquisa no Google Acadêmico" if pesquisa == None else "Resultado da pesquisa: " + pesquisa
        resultado = "Nenhuma pesquisa feita!" if resultado == None else resultado
        options = {"title": title, "Resultado":resultado}
        result = render_template("pesquisa.html", options)
        self.write(result)

    def get(self):
        """ Quando a página google_academico_acha_autores/?pesquisa=texto carregar """
        try:
            pesquisa = self.get_argument("pesquisa")
        except:
            pesquisa = None
        resultado = self.get_resultado(pesquisa)
        self.call_template_pesquisa(pesquisa, resultado)
            
        
STATIC_PATH = os.path.abspath(os.path.dirname(__file__))
routes_google_academico_acha_autores = [
    (r"/google_academico_acha_autores/css/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/css/"}),
    (r"/google_academico_acha_autores/js/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/js/"}),
    (r"/google_academico_acha_autores/img/(.*)", StaticFileHandler, {"path": STATIC_PATH + "/img/"}),
    (r"/google_academico_acha_autores/?.*", PesquisaHandler)
]
