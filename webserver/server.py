import tornado.web          # the Tornado web framework
import tornado.httpserver   # the Tornado web server
import tornado.ioloop       # the Tornado event-loop
import tornado.websocket    # the Tornado event-loop
import json
from json import dumps
import webinterface
import json
from tornado import gen
from tornado.web import asynchronous
import threading
from colorama import Fore
from multiprocessing import Process


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class Worker(threading.Thread):
   def __init__(self, callback=None, msg='', *args, **kwargs):
        super(Worker, self).__init__(*args, **kwargs)
        self.callback = callback
        self.msg = msg

   def run(self):
        request = json.loads(self.msg)
        query = request.get('query', {})

        try:
            # print Fore.YELLOW, "\nRequest: %s\nParams: %s\n" % (query["type"], query["params"]) , Fore.WHITE
            result = getattr(webinterface, query.get("type"))(query.get("params"))
        except Exception, e:
            result = {"Error": "%s"%e}
            print Fore.RED, "\nError: ", e, Fore.WHITE

        self.callback(result)



class HTTPApi(tornado.web.RequestHandler):

    @asynchronous
    def post(self):
        message = self.get_argument("data",{})
        Worker(self.onComplete, message).start()
        # w = Worker(self.onComplete, message)
        # p = Process(target=w.run, args=())
        # p.start()

    def onComplete(self, result):
        self.finish(dumps(result))


class TrainerSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        # print("WebSocket opened")
        pass
    
    def on_message(self, message):
        # print "Attach Handler Request"
        params = json.loads(message)["params"]
        self.params = params

        webinterface.trainer.register_handler(params, self.write_message)


    def on_close(self):
    
        webinterface.trainer.unregister_handler(self.params)


class XlearnHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('xlearn.html')


class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

class ZipServer(tornado.web.StaticFileHandler):
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
        (r'/trainersocket',                                         
            TrainerSocket),

        (r'/cgtjobs/(.*)',             
            ZipServer, {'path': "cgtjobs"}),
        
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
