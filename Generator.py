import Utilities
import Topology
import Segment

'''
returns topologies but in an unordered fashion
'''
def get_topologies(file, amount):
    if type(amount) is not int:
        return None
    collection = Utilities.get_mongodb(file)
    return collection.find({"count": {"$gte": amount}})

'''
call this function to get topologies sorted by count
'''
def load_topologies(amount, config):
    results = get_topologies("mongo_creds.json", amount)
    topologies = []
    for x in results:
        topology = x['topology']
        if is_eligible(topology, config):
            t = Topology.Topology(topology, x['count'])
            topologies.append(t)
    return sorted(topologies, key=lambda Topology: Topology.count, reverse=True)


'''
takes a part of the sequence and the an array of profile data
'''
def make_password_guesses(topology,organized_profile):
    sequence = get_segments(topology.flat_topology)
    #first prime the list
    combo_list = []
    for x in organized_profile[sequence[0].count]:
        if Utilities.match_type(sequence[0].type_,x):
            combo_list.append(x)
    #make combos from the list
    holder = []
    for x in sequence[1:]:
        for z in combo_list:
            for y in organized_profile[y.count]:
                if Utilities.match_type(x.type,y):
                  holder.append(z+y)
        combo_list = holder
        holder.clear()
    return combo_list


'''
gen_passwords
'''
def gen_passwords(amount, config, profile):
    topologies = load_topologies(amount, config)
    organized_profile = organize_profile(profile)
    passwords = set()
    for x in topologies:
        passwords = Utilities.add_to_set(passwords, make_password_guesses(x,organized_profile))
    return passwords

'''
returns a dictionary of lists where the lists contains profile data that has the same length
the key of the dictionary is an integer that is the length of that data contained in its
corresponding list.
example:
{6:[list of strings that are of length 6]}
'''
def organize_profile(json_profile):
    organized_data = {}
    for x in json_profile.keys():
        object = json_profile[x]
        for z in object.keys():
            if len(object[z]) in organized_data.keys():
                organized_data[len(object[z])].append(object[z])
            else:
                organized_data[len(object[z])] = [object[z]]
    return organized_data


'''
wrapper for the recursive function that actually does the work
'''
def get_segments(topology):
    return get_segments_(topology,[],0,'l')


'''

example topology:
?l?l?l?n?n?n?n?s?l

'''
def get_segments_(topology, segments, count, current):
    if topology is None or segments is None or count < 0 or current is None:
        return None
    if len(topology) < 2:
        segments.append(Segment.Segment(current, count))
        return segments
    elif current != topology[1]:
        segments.append(Segment.Segment(current,count))
        return get_segments_(topology[2:], segments, 1, topology[1])
    else:
        return get_segments_(topology[2:], segments, count + 1, topology[1])


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


'''
Determines whether or not a topology is eligible given the restrictions of the target.
'''
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



def cmp(x, y):
    return x.count - y.count
