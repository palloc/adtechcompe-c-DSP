import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver
import time
import json
import pandas as pd

ngdomains_list = json.load(open('json/ngdomains.json'))
budgets_df = pd.read_json('json/budgets.json')


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

# return the list of ngdomains
def return_ngdomains(adv_id):
    return ngdomains_list['adv_'+adv_id]

# retuen True if its domain is NG
def is_ngdomains(adv_id, domain):
    return domain in ngdomains_list['adv_'+adv_id]

def get_budget(adv_id):
    return budgets_df['adv_'+adv_id]['budget']

def get_cpc(adv_id):
    return budgets_df['adv_'+adv_id]['cpc']

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/bid", BidHandler),
        (r"/win", Win_Handler),
    ])
    
    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
