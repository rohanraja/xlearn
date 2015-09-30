import tornado.web          # the Tornado web framework
import tornado.httpserver   # the Tornado web server
import tornado.ioloop       # the Tornado event-loop



# handles incoming request, this is the C part in MVC
class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('index.html')


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
