#coding utf-8
import pickle
import numpy as np

browser_dic = {'Chrome':0,'Firefox':1,'Opera':2,'Safari':3}

with open("clf/dics/cluster_dic_site.dump","r") as f:
    cluster_dic_site = pickle.load(f)

with open("clf/dics/cluster_dic_user.dump","r") as f:
    cluster_dic_user = pickle.load(f)


clfs = []
for n in range(20):
    with open("clf/lr_clf_%d.dump" % int(n + 1)) as f:
        clf = pickle.load(f)
    clfs.append(clf)

#when bid_request comes, make features from browser_dic,cluster_dic_site,cluster_dic_user and predict for each adv

#bid_request = ["Chrome","action.jp",0]


def make_feature(bid_request):
    x = np.array([])

    browser_vec = np.zeros(4)
    browser_index = browser_dic[bid_request[0]]
    browser_vec.put(browser_index,1)
    print browser_vec

    site_vec = np.zeros(100)
    site_index = cluster_dic_site[bid_request[1]]
    site_vec.put(site_index,1)

    user_vec = np.zeros(50)
    user_index = cluster_dic_user[bid_request[2]]
    user_vec.put(user_index,1)

    x = np.append(x, user_vec)
    x = np.append(x, browser_vec)
    x = np.append(x, site_vec)
    return x

def predict(bid_request, advertisers):
    x = make_feature(bid_request)
    print "bid_request"
    x = x.reshape(1,-1)
    ctr = []
    for n in range(1, 21):
        if n in advertisers:
            clf = clfs[n - 1]
            ctr.append(clf.predict_proba(x)[0][1])
        else:
            ctr.append(0)
    return ctr

#ctr = predict(bid_request,[])

#print ctr
