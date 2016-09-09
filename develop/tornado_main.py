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
        
if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
