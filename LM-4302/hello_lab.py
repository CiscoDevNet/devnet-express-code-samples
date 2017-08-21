#!/usr/bin/env python

from myspark import spark_get_room_id, spark_send_message
import requests

# Disable all warning messages since we're dealing with a
# self-signed certificate on APIC-EM
requests.packages.urllib3.disable_warnings()

# We need to know our token and other information.
# Make sure you either create your own room
# or provide the name of the common event room.
# Replace None with the value
SPARK_TOKN = None
SPARK_ROOM = None

if not SPARK_TOKN or not SPARK_ROOM:
    exit("Looks like SPARK_TOKN or SPARK_ROOM variable in hello_lab.py "\
         "is empty.\nPlease assign appropriate values and run the script again.")



# The below URLs, usernames and passwords
# match the dCloud DNA lab
RESTCONF_URL = '198.18.133.218:8008'
RC_USER = 'admin'
RC_PASS = 'C1sco12345'

APIC_EM_URL = '198.18.129.100'
AP_USER = 'admin'
AP_PASS = 'C1sco12345'


def check_restconf(address):
    """
    Function to check if RESTCONF is accessible
    """

    # RESTCONF enabled device's address and default entry level
    restconf_api = 'http://' + address + '/api'

    # Parameter passed during the call
    params = dict(verbose='')

    # Necessary headers to make an API call
    headers = dict(accept='application/vnd.yang.api+json')

    # Actual REST call
    restconf_response = requests.get(restconf_api, headers=headers,
                                     auth=(RC_USER, RC_PASS),
                                     params=params, timeout=5.0)
    return restconf_response.ok


def check_apic_em(address):
    """
    Function to check if APIC-EM is accessible
    """

    # APIC-EM address and default entry level
    apic_em_api = 'https://' + address + '/api/v1/ticket'

    # Necessary headers to make an API call
    headers = {
        'content-type': 'application/json'
    }
    payload = {
        'username': AP_USER,
        'password': AP_PASS
    }
    # Making Rest call
    apic_em_response = requests.post(
        apic_em_api, headers=headers, json=payload, verify=False, timeout=5.0)

    return apic_em_response.ok


# this is the variable of the room id we need to figure out:
room_id = None
# you can replace room ID from output of script here
# this will speed up things a bit as the room search
# can be omitted.
# room_id = 'your-room-id-output-from-the-script'


if not room_id:
    room_id = spark_get_room_id(SPARK_TOKN, SPARK_ROOM)
    print('Your room ID "{id}".'.format(id=room_id))

if room_id:
    spark_send_message(SPARK_TOKN, room_id,
                       'Hello room! My script verified that I can '
                       'post messages to Spark using REST API calls.')
    if check_restconf(RESTCONF_URL):
        spark_send_message(SPARK_TOKN, room_id,
                           'It also verified that RESTCONF enabled device '
                           'is working properly.')
    else:
        spark_send_message(SPARK_TOKN, room_id,
                           'Unfortunately, RESTCONF enabled device is '
                           'NOT working properly.')
    if check_apic_em(APIC_EM_URL):
        spark_send_message(SPARK_TOKN, room_id,
                           'It also verified that APIC-EM '
                           'is working properly.')
    else:
        spark_send_message(SPARK_TOKN, room_id,
                           'Unfortunately, APIC-EM is '
                           'NOT working properly.')
    print('Please check room ' + SPARK_ROOM +
          ', there are messages posted on your behalf.')
