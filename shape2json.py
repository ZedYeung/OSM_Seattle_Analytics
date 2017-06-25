"""Wrangle the data in osm file and transform it into json file."""
import re
import codecs
import pprint
import json
import xml.etree.cElementTree as ET
from collections import defaultdict
from audit_tag import update_tag

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
SAMPLE = 'Seattle_sample1.osm'
FILE = 'Seattle.osm'


def shape_element(element):
    """Shape the element into a dict.

    Args:
        element: node, way, relation element

    Returns:
         A dict contains the shaped data for node, way, relation element.

    """
    print("Shape element {type} {id}".format(
        type=element.tag, id=element.get('id')
        ))
    node = defaultdict(dict)
    node['id'] = element.get('id')
    node['type'] = element.tag
    node['visible'] = 'true'
    for tag in CREATED:
        node['created'][tag] = element.get(tag)

    if element.tag == "node":
        node['pos'] = [float(element.get('lat')), float(element.get('lon'))]
    elif element.tag == 'way':
        node['node_refs'] = []
        for nd in element.iter("nd"):
            node['node_refs'].append(nd.get('ref'))
    else:
        for mem in element.iter("member"):
            node['member']['id'] = mem.get('ref')
            node['member']['type'] = mem.get('type')
            node['member']['role'] = mem.get('role')

    for tag in element.iter("tag"):
        if re.search(problemchars, tag.get('k')):
            print('there are problem chars: {}'.format(tag.get('k')))
            continue
        update_tag(tag, node)

    return node


def process_osm(file_in, pretty=False):
    """Wrangle the data in osm file and transform it into json file.

    Args:
        file_in: the original open street map file.
        pretty: Ture for output the json with indent, otherwise without indent.
            Defaults to false, because indent will consume space.
    """
    file_out = "{0}.json".format(file_in)

    print("Processing...")

    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            if element.tag == "node" or element.tag == 'way' or \
                    element.tag == 'relation':
                el = shape_element(element)
                if el:
                    if pretty:
                        fo.write(json.dumps(el, indent=2)+"\n")
                    else:
                        fo.write(json.dumps(el) + "\n")
        print("Done.")


if __name__ == "__main__":
    process_osm(FILE)
