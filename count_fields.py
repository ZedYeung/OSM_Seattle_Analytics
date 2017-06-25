"""Count fields in osm mongodb database and write to json file."""
import json
import pprint
from collections import OrderedDict
from pymongo import MongoClient

client = MongoClient()

db = client.osm
collection = db.Seattle

key_dict = {}

data = collection.find()

for i in data:
    for key in i.keys():
        key_dict[key] = key_dict.get(key, 0) + 1

field_count = sorted(key_dict.items(), key=lambda x: x[1], reverse=True)

pprint.pprint(field_count)
