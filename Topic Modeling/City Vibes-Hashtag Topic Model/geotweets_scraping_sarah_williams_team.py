
import sys, requests, json, urllib, shutil, datetime, os, time
import redis
import threading
import cStringIO
from twython import Twython
from twython import TwythonError, TwythonRateLimitError, TwythonAuthError
from datetime import datetime
from s3 import upload_to_s3 as upload_to_s3
from math import sqrt, floor
from itertools import product
import os
from pymongo import MongoClient
def getMongoColl(db_name, col_name):
    client = MongoClient('mongodb://root:' + MONGO_PASSWORD + '@' +MONGO_HOST)
    _db = client[db_name]
    _coll = _db[col_name]
    print "conection to mongo"
    return _coll

def writeMongoDoc(colctn, doc):
    colctn.insert_one(doc)
    return

def writeMongoColl(colctn,lis):
    colctn.insert_many(lis)
# from twitter_key import consumer_key, consumer_secret, access_token, access_token_secret
# from s3_key import upload_to_s3

MONGO_HOST='146.148.100.30'
MONGO_PASSWORD='pnZMW55Z'

accclll = [
    [
        'sCAgi9wXbOYzerqSNVbqnVdwh', \
        'C69OfRIJzvKfu3c38mFYgwwKCkIx1mPGps8Yx2KkVj0oXwwQhv', \
        '399546099-eaqHSE0yL6r4RISaIYEBrAmSzw6d2UOj95lvFJc4', \
        'LvUNxq2lgXMnc2ds7we3k0MU3u2H9ILIaEGcmyjxAi5Dw'
    ],
    [
        'qUeiTMZV4PLkzRZ0ECqP5jE8b', \
        'y0h1VYkj0aY5O6UcUZsk91Xevb2irF3qdaqvMZ2zgJLiu8imbW', \
        '882698430-sjfBOZJl1EXynvYXN85jWc1a4Yzy6rkeRQjhcjef', \
        'CyPIsPJJGsRgblOzeSv1GybyG830ncpXeRxdq6YcOxKKG'
    ]
]



sys.path.insert(0, '../')
REDIS_HOST='104.196.24.79' #os.environ['REDIS_HOST']
REDIS_PASS='ED6LaWs0'
PERCISION=20
rapi = redis.StrictRedis(host=REDIS_HOST,password=REDIS_PASS, port=6379, db=0)
# rapi.set('access_counter',0)
access_counter = rapi.incr('access_counter')
if access_counter == 2:
    rapi.set('access_counter',0)

twitter_creds=accclll[access_counter-1]
consumer_key = twitter_creds[0]
consumer_secret = twitter_creds[1] 
access_token = twitter_creds[2]
access_token_secret = twitter_creds[3]
print "twitter_creds clamied: ", twitter_creds
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

# use the this function but as a clusure over the class' method:: for saving the stuff
def get_lots_of_tweets(func):
    def wrap_f(*args, **keywrds):
        results, maxtime = func(*args, **keywrds)
        mcoll = getMongoColl("twitter_results_db", "ryadth")
        all_tweets = {}        
        added = 0
        print results
        for tweet in results["statuses"]:
            writeMongoDoc(mcoll, tweet)
            print 'tweet', tweet
            # try:

            #     tid = tweet['id']

            #     # if tid not in all_tweets and tweet['coordinates'] != None:
            #     properties = {}
            #     properties['lat'] = tweet['coordinates'][0]
            #     properties['lon'] = tweet['coordinates'][1]
            #     properties['tweet_id'] = tid
            #     properties['content'] = tweet['text']
            #     properties['user'] = tweet['user']['id']
            #     properties['user_location'] = tweet['user']['location']
            #     properties['raw_source'] = tweet
            #     properties['data_point'] = 'none'
            #     properties['time'] = tweet['created_at']
            #     all_tweets[ tid ] = properties
            #     added += 1
            # except:
            #     pass

        # t = all_tweets
        # print "t", t
        # target_path = 'twitter_new/%stweets.json' %(str(datetime.now()))
        
        # new_t = json.dumps(t)
        # upload = upload_to_s3( target_path, new_t)
    return wrap_f

def makeMethodCalls(func):
    def wrap_f(*args,  **keywrds):
        results, r, _point, _point_seperation_remainings = func(*args,  **keywrds)
        print "printing results inside the wrap functions", results
        lat=_point[1]
        lng=_point[0]
        for place in results["result"]["places"]:
            print place["id"]
            r.sadd('t_places_capt', place["id"])
        # saving the places and their place idp_s into a set
        if len(results["result"]["places"]) > PERCISION:
            lat2 = float(lat) + _point_seperation_remainings
            lat3 = float(lat) - _point_seperation_remainings
            lng2 = float(lng) + _point_seperation_remainings
            lng3 = float(lng) - _point_seperation_remainings
            print _point_seperation_remainings, lat2, lng2
            coords_more = [
                [lat, lng2],
                [lat, lng3],
                [lat2, lng],
                [lat3, lng],
                [lat2, lng2],
                [lat3, lng3],
                [lat2, lng3],
                [lat3, lng2]
            ]
            for _each in coords_more:
                r.sadd('remainings', _each)
    return wrap_f




class Scrapper(object):
    def __init__(self, _point_seperation, consumer_key, consumer_secret, access_token, access_token_secret):
        self._point_seperation = _point_seperation
        self._dist = _dist = sqrt(2)*(self._point_seperation/0.00001)/2
        self.consumer_key = consumer_key
        self.consumer_secret=consumer_secret
        self.access_token=access_token
        self.access_token_secret=access_token_secret
        self.base_geo = "https://api.twitter.com/1.1/geo/search.json?"        
        self.redis_client = redis.StrictRedis(host=REDIS_HOST,password=REDIS_PASS, port=6379, db=0)
        self.twitter = Twython(app_key=self.consumer_key,
            app_secret=self.consumer_secret,
            oauth_token=self.access_token,
            oauth_token_secret=self.access_token_secret)
        # zero out the counter/incr
        self.redis_client.set('level_cnt', 0)
        self.levels_obj = []
        for i in range(1, 25):
            self.levels_obj.append({
                "_level": i,
                "_dist": _dist,
                "_point_seperation": _point_seperation
                })
            _point_seperation = 0.00001*_dist/2
            _dist = sqrt(2)*(_point_seperation/0.00001)/2
        print "levels_objs", self.levels_obj

    def fishNet(self,_points_seperation, bbox):
        x_min, x_max, y_min, y_max =float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])
        print "setting the self.fishnet"
        x0=drange(x_min, x_max, _points_seperation)
        y0=drange(y_min, y_max, _points_seperation)
        _fish_net = list(product(x0,y0))
        print "_fish_net", _fish_net
        return _fish_net

    @get_lots_of_tweets
    def getTweets(self, maxtime):
        self.maxtime = maxtime
        total_time = 300
        remaining_seconds = total_time
        interval = 30 
        # needs to grab the 
        # max_id_results and/or  max timestamp and/or next_page_link or etc.
        # and keeps making calls till it's the time we want
        while self.redis_client.scard('t_places_capt') > 0 and remaining_seconds > 0:
            place_id = self.redis_client.spop('t_places_capt')
            results = self.twitter.search(q="place:{0}".format(place_id))
            # return "results", results
            # print "At %d seconds, added %d new tweets, for a total of %d" % ( total_time - remaining_seconds, added, len( all_tweets ) )
            time.sleep(interval)
            remaining_seconds -= interval
            return results, maxtime


    @makeMethodCalls        
    def makeCallable(self,_dist):
        self._point_seperation_remainings = 0.00001*_dist
        try:
            results = self.twitter.search_geo(lat=self._point[0],long=self._point[1],accuracy="{0}m".format(int(floor(_dist))),granularity="poi")
            return results, self.redis_client, self._point, self._point_seperation_remainings
        except TwythonRateLimitError, HTTPSConnectionPool:
            print "sleeping for 900 seconds"
            time.sleep(900)
            self.twitter = Twython(app_key=self.consumer_key,
                app_secret=self.consumer_secret,
                oauth_token=self.access_token,
                oauth_token_secret=self.access_token_secret)
            results = self.twitter.search_geo(lat=self._point[0],long=self._point[1],accuracy="{0}m".format(int(floor(_dist))),granularity="poi")
            return results, self.redis_client, self._point, self._point_seperation_remainings


    def getPlaces(self, bbox):        
        # check the remaining points to see if there needs to be more in depth\
        # decides and calculate a new _dist, a new point seperation 
        # loops
        level = self.redis_client.incr('level_cnt')
        for each_obj in self.levels_obj:
            if each_obj["_level"]==level:
                _dist = each_obj["_dist"]
                _point_seperation = each_obj["_point_seperation"]
            else:
                pass
        points = self.fishNet(_point_seperation, bbox) if level == 1 else self.redis_client.smembers('remainings')
        for _point in points:
            time.sleep(30)
            self._point = _point
            self.makeCallable(_dist)



scraper = Scrapper(0.1,consumer_key, consumer_secret, access_token, access_token_secret)
scraper.getPlaces([24.402110,25.158427,46.369580, 47.248053])
scraper.getTweets(1458730533)

