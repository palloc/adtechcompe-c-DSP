import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver
import time
import json
import pandas as pd
import redis
import bid_request
import badgets as bg

my_redis = redis.Redis(host='10.140.0.4', port=6379, password = 'ePYL7NVi')
ngdomains_list = json.load(open('json/ngdomains.json'))
budgets_df = pd.read_json('json/budgets.json')
nurl = 'http://104.155.237.141/win'


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")
class BidHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test bid request.")

    def post(self, *args, **kwargs):
        request = self.request.body
        auction_id = json.loads(request)['id']

        # fetch all advertiser's budgets
        budgets = bg.get_budgets()

        bidPrice = 150000.00
        adv_id = 'adv_03'
        # make response
        response = {
            'id' : auction_id,
            'bidPrice' : bidPrice,
            'advertiserId' : adv_id,
            'nurl' : nurl
        }
        # set header
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(response))

        # log data
        with open("/var/log/bid_access.log", "a+") as file:
            file.write(time.ctime())
            file.write("   ")
            file.write(json.dumps(response))
            file.write("\n")

        # redis logging
        my_redis.set(auction_id, response)

class Win_Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("test win notice.")
    def post(self):
        req = json.loads(self.request.body)
        response = json.loads(my_redis.get(req['id']))

        # consume adv_id's badget
        bg.consume(response['advertiserId'], float(req['price']))

        self.write("thank you.")

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
    bg.connect()
    bg.init_budgets()

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/bid", BidHandler),
        (r"/win", Win_Handler),
    ])

    application.listen(80)
    tornado.ioloop.IOLoop.current().start()
