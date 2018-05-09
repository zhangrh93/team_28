"""
Team 28
Ruihan Zhang 865529
Linrong Chen 854645
Ming Yin 816159
Hongyun Ma 805266
Jinge Zhang 769474
"""

import pymongo
import json

DBNAME = "myDatabase"
COLLECTION = "testrequestCollection"
HOST = "115.146.86.112"
PORT = 27017

client = pymongo.MongoClient(HOST, PORT)
collection = client[DBNAME][COLLECTION]

c = dict()
m = []
cursor = collection.find({})
for d in cursor:

    name = d["_id"]
    sentiment = [d["sentiment"]["positive"],d["sentiment"]["negative"],d["sentiment"]["neutral"]]
    time = [0]*24
    for i in range(24):
        hoursent = d["time"][str(i)]
        pos = hoursent["positive"]
        neg = hoursent["negative"]
        neu = hoursent["neutral"]
        if pos + neg + neu == 0:
            time[i] = 0
        else:
            time[i] = pos / (pos + neg + neu)

    c[name] = {"sentiment":sentiment, "time":time}

    m_dict = dict()
    geo_str = d["location"].split(",")
    lati = float(geo_str[1][:-1])
    long = float(geo_str[0][1:])
    m_dict["cor"] = [lati, long]
    total = sum(sentiment)
    if total == 0:
        ratio = 0
    else:
        ratio = sentiment[0] / total
    m_dict["weight"] = {"ratio":ratio, "total":total}
    m.append(m_dict)

with open("chart_data.json", "w") as f:
    json.dump(c, f)

with open("map_data.json", "w") as f:
    json.dump(m, f)
