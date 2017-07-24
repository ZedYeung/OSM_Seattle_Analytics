"""Use Google map api to cross-validate open street map data.

Cross-validating phone, postal code and street address.
"""
import googlemaps
import time
import xml.etree.cElementTree as ET
from audit_street import update_street
from audit_phone import update_phone_number

SAMPLE = 'Seattle_sample_phone.osm'
gmaps = googlemaps.Client(key='AIzaSyBV3gehRJcZCTEL7Lc1zWqjIDthfjPVAR4')


def get_place(element):
    """Return comprehensive details dict for an individual place.

    Reference:
    https://developers.google.com/places/web-service/details#PlaceDetailsResults
    """
    pos = ((float(element.get('lat')), float(element.get('lon'))))
    reverse_geocode_result = gmaps.reverse_geocode(pos)
    place_id = reverse_geocode_result[0]['place_id']
    place = gmaps.place(place_id)['result']
    return place


def cross_validate(osmfile):
    """Cross-validating phone, postal code and street address.

    Respectively count the total number of phone, postal code and street
    address in OSM and number of inconsistent itmes in OSM and googlemaps.
    """
    google_address = ''
    osm_address_street = ''
    phone_count = 0
    phone_diff_count = 0
    postal_code_count = 0
    postal_code_diff_count = 0
    address_count = 0
    address_diff_count = 0

    with open(osmfile, "r") as osmf:
        for event, element in ET.iterparse(osmf, events=("start",)):
            if element.tag == "node":
                for tag in element.iter("tag"):
                    key = tag.get('k')
                    if key == "phone" or key == "contact:phone":
                        phone_count += 1
                        place = get_place(element)
                        phone_number = place.get('international_phone_number')
                        if phone_number:
                            osm_phone = update_phone_number(tag.get('v'))
                            if phone_number != osm_phone:
                                phone_diff_count += 1
                                print((phone_number, osm_phone))

                    if key == "postal_code" or key == "addr:postcode":
                        postal_code_count += 1
                        place = get_place(element)
                        formatted_address = place.get('formatted_address')
                        if formatted_address:
                            postal_code = formatted_address[-10:-5]
                            osm_postal_code = tag.get('v')
                            if postal_code != osm_postal_code:
                                postal_code_diff_count += 1
                                print((postal_code, osm_postal_code))

                    if key == "addr:street":
                        address_count += 1
                        place = get_place(element)
                        address = place.get('name')
                        street_list = address.split()[1:]
                        street = ' '.join(street_list)
                        if len(street_list) > 1:
                            google_address_street = update_street(street)
                        else:
                            google_address_street = street
                        google_address_number = address.split()[0]
                        google_address = google_address_number + ' ' \
                            + google_address_street
                        osm_address_street = update_street(tag.get('v'))
                    if key == "addr:housenumber":
                        osm_address_number = tag.get('v').split()[0]
                        osm_address = osm_address_number + ' ' \
                            + osm_address_street
                        if google_address != osm_address:
                            address_diff_count += 1
                            print((google_address, osm_address))

    print(phone_count)
    print(phone_diff_count)
    print(postal_code_count)
    print(postal_code_diff_count)
    print(address_count)
    print(address_diff_count)


if __name__ == "__main__":
    cross_validate(SAMPLE)
