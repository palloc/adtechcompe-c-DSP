#coding:utf-8

import numpy as np

import sys 
import csv                                                                               
import pickle 
import matplotlib.pyplot as plt
import matplotlib
import scipy as sp
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages")
import MySQLdb 
from db_config import Mysql_config


mysql_config = Mysql_config()
dbcon,cursor = mysql_config.set_mysql_config()
print 'yay'

device_dic = {'Android':0,'BlackBerry':1,'iOS':2,'Windows':3}
browser_dic = {'Chrome':0,'Firefox':1,'Opera':2,'Safari':3}

with open("dics/cluster_dic_site.dump","r") as f:
    cluster_dic_site = pickle.load(f)

with open("dics/cluster_dic_spot.dump","r") as f:
    cluster_dic_spot = pickle.load(f)

with open("dics/cluster_dic_user.dump","r") as f:
    cluster_dic_user = pickle.load(f)


def get_test_data(sample,userID = False,device=False,browser=False,site=False,spot=False):
    cursor.execute("select userID,device,browser,site,spot,adv_1,adv_2,adv_3,adv_4,adv_5,adv_6,adv_7,adv_8,adv_9,adv_10,adv_11,adv_12,adv_13,adv_14,adv_15,adv_16,adv_17,adv_18,adv_19,adv_20 from ad order by rand() limit %d;" % sample)
    result = cursor.fetchall()
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    for n,row in enumerate(result):
        x = []
        if userID:
            user_vec = np.zeros(50)
            user_vec[cluster_dic_user[row[0]]] = 1
            x.extend(user_vec)
        if device:
            device_vec = np.zeros(4)
            device_vec[device_dic[row[1]]] = 1
            x.extend(device_vec)
        if browser:
            browser_vec = np.zeros(4)
            browser_vec[browser_dic[row[2]]] = 1
            x.extend(browser_vec)
        if site:
            site_vec = np.zeros(100)
            site_vec[cluster_dic_site[row[3]]] = 1
            print cluster_dic_site[row[3]]
            x.extend(site_vec)
        if spot:
            spot_vec = np.zeros(20)
            try:
                spot_vec[cluster_dic_spot[row[4]]] = 1
            except:
                pass
            x.extend(spot_vec)
        print np.shape(x)
        if n < sample * 0.8:
            train_x.append(x)
            train_y.append(row[5:])
        else:
            test_x.append(x)
            test_y.append(row[5:])
        
    return train_x,train_y,test_x,test_y

print "loading data..."

train_x,train_y,test_x,test_y = get_test_data(userID=True,device=False,browser=True,site=True,spot=False,sample = 100000)


print "loaded data"
"""
print np.shape(train_x)
_train_x = np.array(train_x)
train_y = np.array(train_y)
test_y = np.array(test_y)
for n in range(len(_train_x)):
    length = n + 1
    vec = _train_x[:length].astype('float32')
    total = np.sum(vec,axis = 0)
    vec = total / length
    train_x[n] = vec

train_x = np.array(train_x)
for i in train_x:
    print i

test_x = [train_x[len(train_x) - 1] for i in range(len(test_y))]
"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.ensemble import RandomForestClassifier as rfc
from sklearn.grid_search import GridSearchCV,RandomizedSearchCV
from sklearn.externals import joblib
sys.path.append("/home/toyama/ad/xgboost/python-package")
import xgboost as xgb


def grid_search(clf):
    parameters = {
        'n_estimators'      : [5, 20,  100],
        'max_features'      : [3, 10,  20],
        'random_state'      : [0],
        'n_jobs'            : [1],
        'min_samples_split' : [3, 10, 20, 100],
        'max_depth'         : [3, 10, 20, 100]
    }

    clf = GridSearchCV(clf,parameters)
    return clf

def classify(clf,grid = False):
    all_f = 0
    for n in range(20):
        if clf == 'lr':
            clf = LogisticRegression(C=1.0,class_weight = 'balanced')
        elif clf == 'rfc':
            clf = rfc(class_weight = 'balanced')
            if grid:
                print "grid"
                clf = grid_search(clf)
        elif clf == 'xgb':
            param_distributions={'max_depth': sp.stats.randint(1,11),
                     'subsample': sp.stats.uniform(0.5,0.5),
                     'colsample_bytree': sp.stats.uniform(0.5,0.5)}
            xgb_model = xgb.XGBClassifier()
            clf = RandomizedSearchCV(xgb_model,
                        param_distributions,
                        cv=5,
                        n_iter=10,
                        scoring="log_loss",
                        n_jobs=5,
                        verbose=2)
        train_y_1 = [y[n] for y in train_y]
        test_y_1 = [y[n] for y in test_y]
    
        print "fitting"
        clf.fit(np.array(train_x),np.array(train_y_1))
        if grid:
            print clf.best_estimator_
        pred_y = clf.predict(test_x)
        report = classification_report(test_y_1,pred_y)
        print report
        f1 = f1_score(test_y_1,pred_y)
        all_f += f1
        with open("clf/xgb_clf_{}.dump".format(n+1),"w") as f:
            pickle.dump(clf, f)
        
    print all_f
    

classify('xgb',grid = False)
        
"""
error = 0
for n in range(20):
    train_y_1 = [y[n] for y in train_y]
    test_y_1 = [y[n] for y in test_y]


    lr = LogisticRegression(C=1000.0)
    lr.fit(train_x, train_y_1)

    pred_y = lr.predict_proba(test_x)

    
    for p,i in zip(pred_y,test_y_1):
        error += (p[1] - i) ** 2
"""
