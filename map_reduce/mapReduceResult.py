"""
Team 28
Ruihan Zhang 865529
Linrong Chen 854645
Ming Yin 816159
Hongyun Ma 805266
Jinge Zhang 769474
"""

import pymongo
import sys
from bson.code import Code

ip_address = sys.argv[1]
collection_name = sys.argv[2]
inputCollection = sys.argv[3]
location = sys.argv[4]
location.replace('_', ' ')

mongo_client = pymongo.MongoClient(ip_address, 27017)
db = mongo_client['myDatabase']
outputCollection = db[collection_name]

mapper = Code("""
function() {
    emit('""" + location + """', 1);
}
""")
reducer = Code("""
function(key, values) {
    return Array.sum(values);
    }
""")

try:
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result")
	for item in result.find():
		outputCollection.insert_one({'_id' : item['_id'], 'sentiment' : {'positive' : 0, 'neutral' : 0, 'negative' : 0, 'total' : 0}})
except:
    pass

try:
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result", query = {"sentiment" : {"$exists":True}})
	for item in result.find():
		outputCollection.update_one({'_id' : item['_id']}, {'$set' : {'sentiment.total' : item['value']}})
except:
    pass

try:   
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result", query = {"sentiment" : "positive"})
	for .replace('_', ' ')item in result.find():
		outputCollection.update_one({'_id' : item['_id']}, {'$set' : {'sentiment.positive' : item['value']}})
except:
    pass

try:    
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result", query = {"sentiment" : "negative"})
	for item in result.find():
		outputCollection.update_one({'_id' : item['_id']}, {'$set' : {'sentiment.negative' : item['value']}})
except:
    pass

try:    
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result", query = {"sentiment" : "neutral"})
	for item in result.find():
		outputCollection.update_one({'_id' : item['_id']}, {'$set' : {'sentiment.neutral' : item['value']}})
except:
    pass

mapper = Code("""
function() {
    var td = {}
    for (var j = 0; j < 24; j++)
          td[j] = {"positive":0,"negative":0,"neutral":0} 
    if (this.sentiment != undefined)
        td[parseInt(this.created_at.split(' ')[3].split(':')[0])][this.sentiment] = 1
    emit('""" + location + """', td);
}
""")
reducer = Code("""
function(key, values) {
    td = values[0]
    for (var i = 1; i < values.length; i++)
        for (var j = 0; j < 24; j++){
            td[j]["positive"] = td[j]["positive"] + values[i][j]["positive"];
            td[j]["negative"] = td[j]["negative"] + values[i][j]["negative"];
            td[j]["neutral"] = td[j]["neutral"] + values[i][j]["neutral"];
        }
    return td;
}
""")
try:
	result = db[inputCollection].map_reduce(mapper, reducer, out = "result")
	for item in result.find():
		outputCollection.update_one({'_id' : item['_id']}, {"$set":{'time' : item['value']}})
except:
    pass


