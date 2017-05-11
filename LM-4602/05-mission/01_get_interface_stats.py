#!/usr/bin/env python
#


from ncclient import manager
import sys
import xml.dom.minidom
import xmltodict
from pprint import pprint
import requests
import json

# MISSION: Assign your authentication token obtained from Spark's Developer page
AUTH = None
# MISSION: Fill in the Name of the Room in which your message will be posted.
ROOM_NAME = None

# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
HOST = '198.18.133.218'
# use the NETCONF port for your CSR1000V device
PORT = 2022
# use the user credentials for your CSR1000V device
USER = 'admin'
PASS = 'C1sco12345'
# XML file to open
FILE = '01_get_interface_stats.xml'

# Returns the Spark room ID for the user selected Spark room.
def get_roomID(roomName):
    # API Call for rooms
    api_call = "rooms?max=1000"

    if AUTH == None:
        print("Please assign your Spark authorization token to variable AUTH.")
        exit(1)


    # Cisco Spark's API URL address
    url = "https://api.ciscospark.com/v1/" + api_call

    # Content type as well as the authorization must be included in the header
    header = {"content-type": "application/json; charset=utf-8",
              "Authorization": "Bearer " + AUTH}

    # this statement performs a GET on the specified network device url
    response = requests.get(url, headers=header, verify=True)
    r_json = response.json()

    for item in r_json["items"]:
        if roomName == item["title"]:
            return(item["id"])


#Posts message to the passed in Spark room.
def post_spark(text, room_id):
    # API Call to for messages
    api_call = "messages"

    # Cisco Spark's API URL address
    url = "https://api.ciscospark.com/v1/" + api_call

    # Content type as well as the authorization must be included in the header
    header = {"content-type": "application/json; charset=utf-8",
              "Authorization": "Bearer " + AUTH}

    payload = {
        "roomId": room_id,
        "markdown": text
    }
    # this statement performs a GET on the specified network device url
    response = requests.post(url, data=json.dumps(
        payload), headers=header, verify=True)

    print("\nCheck the Spark Room.  You've just posted a message!")


# Function to retrieve information via NETCONF
def get_netconf(xml_filter):
    """
    Main method that retrieves information via NETCONF get.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            # MISSION: Replace XXX with the correct NETCONF operation
            return(m.XXX(f.read()))


def create_message(interface):
    """
    Create a Markdown formatted message about interface state
    """
    # MISSION: Replace XXX with the correct leaf
    message = "## Interface Stats: Interface %s \n" % (interface["name"])
    message += "* Speed: %s \n" % (interface["XXX"])
    message += "* Status: %s \n" % (interface["XXX"])
    message += "* MAC Address: %s \n" % (interface["XXX"])
    message += "* Statistics \n"
    message += "    * Octets In: %s \n" % (interface["statistics"]["in-octets"])
    message += "    * Octets Out: %s \n" % (interface["statistics"]["out-octets"])
    message += "    * Errors In: %s \n" % (interface["statistics"]["in-errors"])
    message += "    * Errors Out: %s \n" % (interface["statistics"]["out-errors"])
    return(message)


def main():
    """
    Mission Entry Point
    """
    ############################################################
    # Mission Step 1: Get Spark Room Id
    ############################################################
    print("Mission Step 1: Retrieving Room ID")
    roomId = get_roomID(ROOM_NAME)

    # Mission Step Verification
    if roomId is None:
        print("  FAILED!!!  ")
        sys.exit("Mission Failed")
    else:
        print("Spark Room ID is: " + roomId)
        print("")


    ############################################################
    # Mission Step 2: Make the NETCONF Connection
    ############################################################
    print("Mission Step 2: Making NETCONF Connection to Router")
    # Make NETCONF connection
    netconf = get_netconf(FILE)

    # PREREQ: perform a `pip install xmltodict` in the virtualenv
    # Create an Python Ordered Dict object containing the interface details
    interface = xmltodict.parse(netconf.xml)["rpc-reply"]["data"]["interfaces-state"]["interface"]

    # Mission Step Verification
    if not interface["name"] == "GigabitEthernet1":
        print("  FAILED!!!  ")
        sys.exit("Mission Failed")
    else:
        print("The Interface Details: ")
        pprint(interface)
        print("")


    ############################################################
    # Mission Step 3: Create the Spark Message (Markdown Formatted)
    ############################################################
    print("Mission Step 3: Create the Spark Message (Markdown Formatted)")
    message = create_message(interface)
    print("The message will be: ")
    print(message)
    print("")



    ############################################################
    # Mission Complete: Post to Spark Room
    ############################################################
    print("Mission Complete: Post to Spark Room")
    post_spark(message, roomId)

if __name__ == '__main__':
    sys.exit(main())
