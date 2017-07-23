"""Audit street."""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import street_complete

SAMPLE = 'Seattle_sample1.osm'
SAMPLE10 = "Seattle_sample10.osm"
FILE = "Seattle.osm"

road_types = street_complete.road_types
directions = street_complete.directions


def audit_street_type(st_types, dir_types, street_name):
    """Audit street type.

    Args:
        st_types: dict that store {street types: (street name set)}.
        dir_types: dict that store {direction types: (street name set)}.
        street_name: street name.
    """
    st_split = street_name.split()
    # Find the diretion neither first nor last
    for i in st_split[1:-1]:
        if i in directions or i in directions.values():
            print('direction {0}, position {1}'.format(i, st_split.index(i)))

    # Find the unknown street type and direction type that not in road_types
    # and directions, then add all street names associated with that type.
    if st_split[-1] in directions or st_split[-1] in directions.values():
        street_type = st_split[-2]
        direction_type = st_split[-1]
    else:
        street_type = st_split[-1]
        direction_type = st_split[0]
    if street_type in road_types:
        st_types[street_type].add(street_name)
    if direction_type in directions:
        dir_types[direction_type].add(street_name)


def audit(osmfile):
    """Audit street in osm file.

    Returns:
        st_types: dict that store {street types: (street name set)}.
        dir_types: dict that store {direction types: (street name set)}.

    """
    st_types = defaultdict(set)
    dir_types = defaultdict(set)

    with open(osmfile) as osmf:
        for event, element in ET.iterparse(osmf, events=("start",)):
            for tag in element.iter("tag"):
                if tag.get('k') == "addr:street":
                    audit_street_type(st_types, dir_types, tag.get('v'))

    return st_types, dir_types


def update_street(street_name):
    """Return more completed street name."""
    if isinstance(street_name, list):
        street_name = [update_street(i) for i in street_name]
        return street_name
    st_split = street_name.split()
    if st_split[-1] in directions or st_split[-1] in directions.values():
        street_type = st_split[-2]
        direction_type = st_split[-1]
        if road_types.get(street_type):
            st_split[-2] = road_types.get(street_type)
        if directions.get(direction_type):
            st_split[-1] = directions.get(direction_type)
    else:
        street_type = st_split[-1]
        direction_type = st_split[0]
        if road_types.get(street_type):
            st_split[-1] = road_types.get(street_type)
        if directions.get(direction_type):
            st_split[0] = directions.get(direction_type)
    return ' '.join(st_split)


def test(osmfile):
    """Test all function difine above."""
    st_types, dir_types = audit(osmfile)
    pprint.pprint(st_types)
    pprint.pprint(dir_types)
    with open(osmfile, 'r') as osmf:
        for event, element in ET.iterparse(osmf, events=("start",)):
            for tag in element.iter("tag"):
                if tag.get('k') == "addr:street":
                    update_name = update_street(tag.get('v'))
                    print(update_name)


if __name__ == '__main__':
    test(SAMPLE)
