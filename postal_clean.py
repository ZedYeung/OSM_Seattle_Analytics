# clean postcode
# Surprisingly and a little bit depressed, the postcode is 100% pure.
import xml.etree.cElementTree as ET
import re

SAMPLE = 'Seattle_sample1.osm'
SAMPLE10 = "Seattle_sample10.osm"
FILE = "Seattle.osm"

def audit_postal_code(postal_code):
    if not postal_code.startswith('98'):
        print(postal_code)
    if not re.match(r'[0-9]{5}', postal_code):
        print(postal_code)


def audit(osmfile):
    osm_file = open(osmfile, "r")
    for event, element in ET.iterparse(osm_file, events=("start",)):
        if element.tag == "node" or element.tag == "way":
            for tag in element.iter("tag"):
                if tag.get('k') == "postal_code" or tag.get('k') == "addr:postcode":
                    audit_postal_code(tag.get('v'))
    osm_file.close()

if __name__ == '__main__':
    audit(FILE)
