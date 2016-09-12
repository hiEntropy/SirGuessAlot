import Utilities
import Topology


def get_topologies(file, amount):
    if type(amount) is not int:
        return None
    collection = Utilities.get_mongodb(file)
    return collection.find({"count": {"$gte": amount}})


def load_topologies(amount, config):
    results = get_topologies("mongo_creds.json", amount)
    topologies = []
    for x in results:
        topology = x['topology']
        if is_eligible(topology, config):
            t = Topology.Topology(topology, x['count'])
            topologies.append(t)
    return sorted(topologies, key=lambda Topology: Topology.count, reverse=True)


def is_eligible(topology, config):
    config = Utilities.get_JSON_Obj(config)
    if config is None:
        return None
    specials = config['specials']
    lowers = config['lowers']
    caps = config['cap_required']
    numbers = config['numbers']
    min_len = config['min_password_len']
    max_len = config['max_password_len']
    length = len(topology) / 2
    has_cap = False
    has_lower = False
    has_num = False
    has_spec = False
    if length > max_len or length < min_len:
        return False
    for x in [item for item in range(0, len(topology)) if item % 2]:
        current = topology[x]
        if current == 'n':
            has_num = True
        elif current == 's':
            has_spec = True
        elif current == 'u':
            has_cap = True
        elif current == 'l':
            has_lower = True
    if specials == "req" and not has_spec:
        return False
    if specials == 'not-allowed' and has_spec:
        return False
    if numbers == 'req' and not has_num:
        return False
    if numbers == 'not-allowed' and has_num:
        return False
    if caps == 'req' and not has_cap:
        return False
    if caps == 'not-allowed' and has_cap:
        return False
    if lowers == 'req' and not has_lower:
        return False
    if lowers == 'not-allowed' and has_lower:
        return False
    return True


def gen_passwords(amount, config, profile):
    topologies = load_topologies(amount, config)
    password_list = []


def organize_profile(json_profile):
    organized_data = {}
    for x in json_profile.keys():
        if len(json_profile[x]) in organized_data.keys():
            organized_data[len(json_profile[x])].append(json_profile[x])
        else:
            organized_data[len(json_profile[x])] = [json_profile[x]]
    return organized_data

def get_topology(string):
    topology = ""
    if string is not None:
        for x in string:
            if x.isupper():
                topology += "?u"
            elif x.islower():
                topology += "?l"
            elif x.isnumeric():
                topology += "?n"
            elif x != '\n':
                topology += "?s"
    return topology


def cmp(x, y):
    return x.count - y.count
