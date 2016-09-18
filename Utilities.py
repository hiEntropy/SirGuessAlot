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


def add_to_set(theSet,theList):
    for x in theList:
        theSet.add(x)
    return theSet


def flatten(topologies):
    flattened_topologies = []
    for x in topologies:
        flattened_topologies.append(flatten_(x))
    return  flattened_topologies


'''
converts ?s and ?u to ?l so that we can come up with generic solutions then apply likely substitutions
after generating the most naive passwords.
'''
def flatten_(topology):
    if len(topology) < 1:
        return topology
    elif topology[0] == 'u' or topology[0] == 's':
        return 'l' + flatten_(topology[1:])
    else:
        return topology[0] + flatten_(topology[1:])

'''
Should only be used to check flattened topologies
'''
def match_type(type_,check):
    if type_ == 'n' and check.isnumeric():
        return True
    if type_ == 'l' and check.isalpha():
        return True
    else:
        return False