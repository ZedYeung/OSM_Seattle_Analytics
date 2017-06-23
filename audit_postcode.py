"""Audit postcode.

Surprisingly and a little bit depressed, the postcode is 100% pure.
"""
import xml.etree.cElementTree as ET
import re

SAMPLE = 'Seattle_sample1.osm'
SAMPLE10 = "Seattle_sample10.osm"
FILE = "Seattle.osm"


def audit_postal_code(postal_code, problem_postal_code):
    """Audit postal code."""
    if not re.match(r'[0-9]{5}', postal_code):
        problem_postal_code.append(postal_code)
    if not postal_code.startswith('98'):
        problem_postal_code.append(postal_code)


def audit(osmfile):
    """Audit postal code in osm file."""
    problem_postal_code = []
    with open(osmfile, "r") as osmf:
        for event, element in ET.iterparse(osmf, events=("start",)):
            if element.tag == "node" or element.tag == "way":
                for tag in element.iter("tag"):
                    if tag.get('k') == "postal_code" or \
                            tag.get('k') == "addr:postcode":
                        audit_postal_code(tag.get('v'), problem_postal_code)
        return problem_postal_code


if __name__ == '__main__':
    problem_postal_code = audit(SAMPLE)
    print(problem_postal_code)
