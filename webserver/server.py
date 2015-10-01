import tornado.web          # the Tornado web framework
import tornado.httpserver   # the Tornado web server
import tornado.ioloop       # the Tornado event-loop
import json
from bson.json_util import dumps
import webinterface


# handles incoming request, this is the C part in MVC
class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('index.html')



class HTTPApi(tornado.web.RequestHandler):

    def post(self):
        message = self.get_argument("data",{})

        request = json.loads(message)
        query = request.get('query', {})

        try:
            result = getattr(webinterface, query.get("type"))(query.get("params"))
        except Exception, e:
            result = "Some Error %s" % e

        self.write(dumps(result))


class XlearnHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('xlearn.html')


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

handlers = [

        (r"/", 
            MainHandler),
        (r"/xlearn", 
            XlearnHandler),
        (r'/http_api',                                         
            HTTPApi),
        
        (r'/(.*)',             
            MyStaticFileHandler, {'path': "static/app"}),


        ]


def run():

    app = tornado.web.Application(
            handlers,
            debug=True, 
            template_path='static/app'
            )
    srv = tornado.httpserver.HTTPServer(app, xheaders=True)
    srv.bind(8000, '')

    srv.start(1)

    tornado.ioloop.IOLoop.instance().start()
