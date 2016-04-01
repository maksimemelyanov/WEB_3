import os

HOST = "localhost"
PORT = 8000

TOP = "<div class='top'>Middleware TOP</div>"
BOTTOM = "<div class='botton'>Middleware BOTTOM</div>"

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


def app(environ, start_response):

    res = environ['PATH_INFO']
    path = './' + res

    if not os.path.isfile(path):
        path ='./index.html'

    fd = open(path,'r')
    fileContent = fd.read()
    fd.close()
    start_response('200 OK', [('Content-Type', 'text/html')])
    return fileContent

app = MiddleWare(app)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host=HOST, port=PORT)
