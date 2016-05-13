from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
import os

from pyramid.wsgi import wsgiapp

HOST = '0.0.0.0'
PORT = 8000

TOP = "<div class='top'>Middleware TOP</div>"
BOTTOM = "<div class='botton'>Middleware BOTTOM</div>"

def index_html(environ, start_response):
    file = open('./index.html', 'r')
	data = file.read()
	file.close()
	
	return Response(data)

def aboutme_html(environ, start_response):
    file = open('./about/aboutme.html', 'r')
	data = file.read()
	file.close()
	
	return Response(data)


MIDDLEWARE_TOP = "<div class='top'>Middleware TOP</div>"
MIDDLEWARE_BOTTOM =  "<div class='botton'>Middleware BOTTOM</div>"


if __name__ == '__main__':
    config = Configurator()
    config.add_route('ind1', '/')
    config.add_route('ind2', '/index.html')
    config.add_route('about', '/about/aboutme.html')
	config.add_view(index_html, route_name='ind1')
	config.add_view(index_html, route_name='ind2')
    config.add_view(aboutme_html, route_name='about')
    app = config.make_wsgi_app()
    MWApp = MiddleWare(app)
    server = make_server(HOST, PORT, MWApp)
    server.serve_forever()


class MiddleWare(object):
    def __init__(self, app):
       self.app = app

    def __call__(self, environ, start_response):
        response = self.app(environ, start_response)
        header,body = response.split('<body>')
        body,footer = body.split('</body>')
        body = '<body>'+ TOP + body + BOTTOM+'</body>'
        page = header+ body + footer
        return page



