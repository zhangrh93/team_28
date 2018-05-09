"""
Team 28
Ruihan Zhang 865529
Linrong Chen 854645
Ming Yin 816159
Hongyun Ma 805266
Jinge Zhang 769474
"""

import pymongo
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import sys

if __name__ == '__main__':
    with open("locations.json","r") as file:
        location_str = json.load(file)
    
    ip_address = sys.argv[1]
    collection_name = sys.argv[2]
    location_list = location_str[sys.argv[3]].split(',')
    num = sys.argv[4]

    mongo_client = pymongo.MongoClient(ip_address, 27017)
    db = mongo_client['myDatabase']
    collection = db[collection_name]

    with open("twKey.json","r") as f:
        key = json.load(f)
    consumer_key = key[num]["consumer_key"]
    consumer_secret = key[num]["consumer_secret"]
    access_token = key[num]["access_token"]
    access_token_secret = key[num]["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    class listener(StreamListener):
        def on_data(self, data):
            try:
                if json.loads(data)['lang'] == 'en':
                    dic = json.loads(data)
                    dic.update({'_id' : json.loads(data)['id']})
                    try:
                        collection.insert_one(dic)
                    except:
                        pass

                return True
            except:
                pass

        def on_error(self, status):
            print (status)

    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations = [float(location_list[0]),float(location_list[1]),float(location_list[2]),float(location_list[3])])


