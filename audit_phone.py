"""Audit phone.

Transform the phone number mainly into format "+1 206-XXX-XXXX" or
other toll-free number format like "+1 888-XXX-XXXX" and "911".
"""
import xml.etree.cElementTree as ET
import re

SAMPLE = 'Seattle_sample1.osm'
SAMPLE10 = "Seattle_sample10.osm"
FILE = "Seattle.osm"


def update_phone_number(phone):
    """Return formatted phone number."""
    phone_num = re.sub('\D', '', phone)
    if phone_num == '' or phone_num == "911":
        pass
    elif phone_num.startswith('1'):
        phone_num = '+1 ' + phone_num[1:4] + '-' + \
            phone_num[4:7] + '-' + phone_num[7:11]
    elif phone_num.startswith('001'):
        phone_num = '+1 ' + phone_num[3:6] + '-' + \
            phone_num[6:9] + '-' + phone_num[9:13]
    else:
        phone_num = "+1 " + phone_num[0:3] + '-' + \
            phone_num[3:6] + '-' + phone_num[6:10]
    return phone_num


def audit(osmfile):
    """Audit phone_num number in osm file."""
    problem_phone = []
    problem_update_phone = []
    with open(osmfile, "r") as osmf:
        for event, element in ET.iterparse(osmf, events=("start",)):
            if element.tag == "node" or element.tag == "way":
                for tag in element.iter("tag"):
                    if tag.get('k') == "phone" or \
                            tag.get('k') == "contact:phone":
                        phone = tag.get('v')
                        update_phone = update_phone_number(phone)
                        print(update_phone)
                        if update_phone == '' or update_phone == "911":
                            pass
                        else:
                            if len(update_phone) != 15:
                                problem_phone.append(phone)
                                problem_update_phone.append(update_phone)
                            if not update_phone.startswith("+1 "):
                                problem_phone.append(phone)
                                problem_update_phone.append(update_phone)
                            if update_phone[6] != '-':
                                problem_phone.append(phone)
                                problem_update_phone.append(update_phone)
                            if update_phone[10] != '-':
                                problem_phone.append(phone)
                                problem_update_phone.append(update_phone)
    return problem_phone, problem_update_phone


if __name__ == '__main__':
    problem_phone, problem_update_phone = audit(FILE)
    print(problem_phone)
    print(problem_update_phone)
