import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])

    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()