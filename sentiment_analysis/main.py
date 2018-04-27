import tensorflow as tf
import pymongo
from lstm_model import LSTM
from processer import Processer

DBNAME = "twitter"
COLLECTION = "twitters"
HOST = "localhost"
PORT = 27017
CONFIDENCE = 0.98

client = pymongo.MongoClient(HOST, PORT)
db = client[DBNAME]
collection = db[COLLECTION]

sess = tf.Session()
model = LSTM(sess)
processer = Processer()

d = collection.find_one({"sentiment":{"$exists":False}})
while d:
    uid = d["_id"]
    text = d["text"]
    seq, mask = processer.process(text)
    probs = model.predict(seq, mask, sess)

    if probs[0] > CONFIDENCE:
        sentiment = "positive"
    elif probs[1] > CONFIDENCE:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    d["sentiment"] = sentiment

    collection.replace_one({"_id":uid}, d)
    d = collection.find_one({"sentiment":{"$exists":False}})
