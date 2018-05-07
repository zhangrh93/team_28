import pymongo
import tweepy
import datetime
import sys

if __name__ == '__main__':
    ip_address = sys.argv[1]

    mongo_client = pymongo.MongoClient(ip_address, 27017)
    db = mongo_client['myDatabase']
    suburb_collection = db['suburbCollection']

    with open("twKey.json","r") as f:
        key = json.load(f)
    consumer_key = key[num]["consumer_key"]
    consumer_secret = key[num]["consumer_secret"]
    access_token = key[num]["access_token"]
    access_token_secret = key[num]["access_token_secret"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    places = api.geo_search(lat = -37.809958, long = 144.963801, granularity = "neighborhood", max_results = 100)

    suburb_id = []

    for i in range(len(places)):
        place_id = places[i].id
        suburb_id.append(place_id)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)

    for item in suburb_id:
        tweets = tweepy.Cursor(api.search, q = "place:%s" % item, lang = 'en', since = yesterday, until = today).items()
        for tweet in tweets:
            if tweet.place.id == item:
                print(tweet._json['created_at'], tweet.place.id, tweet.place.full_name)
                tweet._json.update({'_id' : tweet._json['id']})
                try:
                    suburb_collection.insert_one(tweet._json)
                except:
                    continue

