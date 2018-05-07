import tensorflow as tf
import pymongo
from lstm_model import LSTM
from processer import Processer

DBNAME = "myDatabase"
COLLECTION_LIST=["ausCollection","melCollection","synCollection","suburbCollection","vicCollection"]
HOST = "115.146.86.112"
PORT = 27017
POSCONFIDENCE = 0.99
NEGCONFIDENCE = 0.8

client = pymongo.MongoClient(HOST, PORT)
sess = tf.Session()
model = LSTM(sess)
processer = Processer()

db = client[DBNAME]

for COLLECTION in COLLECTION_LIST:

    collection = db[COLLECTION]

    d = collection.find_one({"sentiment":{"$exists":False}})
    while d:
        uid = d["_id"]
        text = d["text"]
        seq, mask = processer.process(text)
        probs = model.predict(seq, mask, sess)

        if probs[0] > POSCONFIDENCE:
            sentiment = "positive"
        elif probs[1] > NEGCONFIDENCE:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        d["sentiment"] = sentiment

        collection.replace_one({"_id":uid}, d)
        d = collection.find_one({"sentiment":{"$exists":False}})
