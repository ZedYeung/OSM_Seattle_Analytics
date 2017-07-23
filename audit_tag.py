"""Update tag like this <tag k="crossing" v="traffic_signals" />.

Example:
    <tag k="addr:city" v="Seattle" />
    <tag k="addr:street" v="West Raye Street" />
    <tag k="addr:postcode" v="98199" />
    <tag k="addr:housenumber" v="2218" />
"""
import re
from audit_street import update_street
from audit_phone import update_phone_number

split_pattern = re.compile(r';|(\|)\1*')


def v_filter(s):
    """Filter problem v."""
    if s == '' or s == '|' or s is None:
        return False
    else:
        return True


def value_list(value):
    """Split v by ';' or one or more '|' and return a list."""
    v_list = re.split(split_pattern, value.strip())
    v_list = list(set(list(filter(v_filter, v_list))))
    return v_list


def update_tag(tag, node):
    """Update tag case by case.

    Args:
        tag: e.g <tag k="crossing" v="traffic_signals" />
        node: a dict contains the shaped data for node, way, relation element.
    """
    key = tag.get('k')
    value = tag.get('v')

    if ';' in value or '|' in value:
        if key == "opening_hours":
            try:
                opening_hours = value.split(';')
                opening_hours = list(filter(None, opening_hours))
                value = [{i.strip().split()[0]: i.strip().split()[1]}
                         for i in opening_hours]
            except Exception as e:
                print(e)
                print(value)
                print(opening_hours)
        elif key == 'old_ref':
            if '(' in value:
                old_ref = re.search(r'(?<=\().*(?=\))', value).group()
                old_ref = re.sub('old ', '', old_ref, flags=re.I)
                value = re.sub('\((.*)\)', '', value)
                value = value_list(value)
                value.append({'old_ref': old_ref.split(';')})
            else:
                value = value_list(value)
        else:
            value = value_list(value)

    if ':' not in key:
        if key == 'addr' or key == 'address':
            node['address']['address'] = value
        elif key == "phone":
            node[key] = update_phone_number(value)
        else:
            node[key] = value

    else:
        key_split = key.split(':')
        if len(key_split) == 2:
            key1, key2 = key_split[0], key_split[1]
            if key1 == 'addr':
                if key2 == 'street':
                    value = update_street(value)
                node['address'][key2] = value
            elif key1 == 'contact':
                if key2 == 'phone':
                    node[key1][key2] = update_phone_number(value)
            # node[key1] maybe assigned as string before,
            # so we change it to a nested dict.
            elif isinstance(node[key1], str) or isinstance(node[key1], list) \
                    or node[key1] is None:
                    node_value = node[key1]
                    del node[key1]
                    node[key1][key1] = node_value
                    node[key1][key2] = value
            # node[key1] is dict
            else:
                node[key1][key2] = value

        # There are more than one  ':'， convert it subjectively
        else:
            if key_split[0] == 'seamark':
                node['seamark']['_'.join(key_split[1:])] = value
            elif key_split[0] in ['sdot', 'service']:
                node['_'.join(key_split[:2])]['_'.join(key_split[2:])] = value
            elif key_split[0] == 'addr':
                node['address']['_'.join(key_split[1:])] = value
            elif 'lane' in key:
                node['lanes_attr']['_'.join(key_split[:])] = value
            else:
                node['_'.join(key_split[:])] = value
