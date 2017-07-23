"""Full word mapping for street suffix and direction abbreviations.

Attributes:
    road_types: a dict stores street "suffix abbreviations: full word" mapping.
    directions: a dict stores "direction abbreviations: full word" mapping.

Reference:
    https://github.com/emacsen/tiger-expansion/blob/master/expansions.py

"""
road_types = {
    'Aly': 'Alley',
    'Arc': 'Arcade',
    'Ave': 'Avenue',
    'Blf': 'Bluff',
    'Blvd': 'Boulevard',
    'Br': 'Bridge',
    'Brg': 'Bridge',
    'Byp': 'Bypass',
    'Cir': 'Circle',
    'Cres': 'Crescent',
    'Cswy': 'Causeway',
    'Ct': 'Court',
    'Ctr': 'Center',
    'Cv': 'Cove',
    'Dr': 'Drive',
    'Expy': 'Expressway',
    'Expwy': 'Expressway',
    'FMRd': 'Farm to Market Road',
    'Fwy': 'Freeway',
    'Grd': 'Grade',
    'Hbr': 'Harbor',
    'Holw': 'Hollow',
    'Hwy': 'Highway',
    'Ln': 'Lane',
    'Lndg': 'Landing',
    'Mal': 'Mall',
    'Mtwy': 'Motorway',
    'Ovps': 'Overpass',
    'Pky': 'Parkway',
    'Pkwy': 'Parkway',
    'Pl': 'Place',
    'Plz': 'Plaza',
    'Rd': 'Road',
    'Rdg': 'Ridge',
    'RMRd': 'Ranch to Market Road',
    'Rte': 'Route',
    'Skwy': 'Skyway',
    'Sq': 'Square',
    'St': 'Street',
    'St.': 'Street',
    'Ter': 'Terrace',
    'Tfwy': 'Trafficway',
    'Thfr': 'Thoroughfare',
    'Thwy': 'Thruway',
    'Tpke': 'Turnpike',
    'Trce': 'Trace',
    'Trl': 'Trail',
    'Tunl': 'Tunnel',
    'Unp': 'Underpass',
    'Wkwy': 'Walkway',
    'Xing': 'Crossing',
    # NOT EXPANDED
    'Way': 'Way',
    'Walk': 'Walk',
    'Loop': 'Loop',
    'Oval': 'Oval',
    'Ramp': 'Ramp',
    'Row': 'Row',
    'Run': 'Run',
    'Pass': 'Pass',
    'Spur': 'Spur',
    'Path': 'Path',
    'Pike': 'Pike',
    'Rue': 'Rue',
    'Mall': 'Mall',
    'Esp': 'Esplanade',
    'BDWY': 'Broadway'
}

directions = {
    'N': 'North',
    'S': 'South',
    'E': 'East',
    'W': 'West',
    'NE': 'Northeast',
    'NW': 'Northwest',
    'SE': 'Southeast',
    'SW': 'Southwest'
}
