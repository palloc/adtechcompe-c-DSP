import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")
class BidHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test bid request.")
    def post(self):
        self.write("test bid request.")
class Win_Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("test win notice.")

        
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/bid", BidHandler),
        (r"/win", Win_Handler),
    ])
    
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
