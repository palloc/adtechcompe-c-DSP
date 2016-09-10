import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.httpserver
import time
import json
import pandas as pd
import bid_request
import badgets as bg
import sys
sys.path.append('../clf')
import predict as pred


ngdomains_list = json.load(open('json/ngdomains.json'))
budgets_df = pd.read_json('json/budgets.json')
nurl = 'http://104.155.237.141/win/'

hashed_ng_domains = {
    k: set(v) for k, v in json.load(open('json/ngdomains.json')).iteritems()}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test")
class BidHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("test bid request.")

    def post(self, *args, **kwargs):
        request = self.request.body
        j = json.loads(request)
        auction_id = j['id']
        floorprice = j['floorPrice']
        # check NG domains and decide advertiser to join
        advertisers = [
            int(adv[4:]) for adv, ngdomains in hashed_ng_domains.iteritems()
            if j['site'] not in ngdomains
        ]

        # fetch all advertiser's budgets
        budgets = bg.get_budgets()

        bid_user = int(j["user"])
        bid_request_for_predict = [j["browser"], j["site"],bid_user]

        # predict CTR
        ctr_list = pred.predict(bid_request_for_predict, advertisers)

        value_list = []
        for (i, ctr) in enumerate(ctr_list):
            value_list.append(ctr * budgets_df['adv_'+str(i+1).zfill(2)]['cpc'])

        bidPrice = max(value_list)
        adv_id_ = value_list.index(max(value_list)) + 1
        adv_id = 'adv_' + str(adv_id_).zfill(2)


        if budgets[adv_id] < bidPrice:
            self.set_status(204)
            self.finish()

        # make response
        response = {
            'id' : auction_id,
            'bidPrice' : bidPrice,
            'advertiserId' : adv_id,
            'nurl' : nurl + adv_id
        }
        if floorprice < response['bidPrice']:
            # set header
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps(response))
        else:
            self.set_status(204)
            self.finish()

        # log data
        with open("/var/log/bid_access.log", "a+") as file:
            file.write(time.ctime())
            file.write("   ")
            file.write(json.dumps(response))
            file.write("\n")
        with open("/var/log/bid_price.log", "a+") as file:
            buf = " bid price = " + str(bidPrice) + "     adv_id = " + adv_id
            file.write(buf)
        
class Win_Handler(tornado.web.RequestHandler):
    def get(self):
        self.write("test win notice.")
    def post(self, adv_id):
        req = json.loads(self.request.body)

        # consume adv_id's badget
        bg.consume(adv_id, float(req['price']))

class DebugHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("debug")

if __name__ == "__main__":
    bg.connect()
    bg.init_budgets()

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/bid", BidHandler),
        (r"/win/(.*)", Win_Handler),
        (r"/debug", DebugHandler),
    ])

    server = tornado.httpserver.HTTPServer(application)
    server.bind(80)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
