import json
import pymongo
from pprint import pprint


def get_JSON_Obj(file):
    try:
        json_str = ""
        with open(file) as fp:
            json_str = json.load(fp)
        return json_str
    except IOError:
        return None
    except OSError:
        return None
    except FileExistsError:
        return None


def get_mongodb(file):
    json_obj = get_JSON_Obj(file)
    client = pymongo.MongoClient(json_obj['url'])
    db = client[json_obj['database']]
    collection = db[json_obj['collection1']]
    return collection
