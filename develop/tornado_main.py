import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver
import time


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")
class BidHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test bid request.")
    def post(self, *args, **kwargs):
        self.write("test bid request.")
        #log data
        with open("/var/log/bid_access.log", "a+") as file:
            file.write(time.ctime())
            file.write("   ")
            file.write(self.request.body)
            file.write("\n")

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
