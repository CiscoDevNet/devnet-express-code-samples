import json
from myspark import spark_get_room_id, spark_send_message
import requests
import sys

#Disbale all warning messages
requests.packages.urllib3.disable_warnings()

# we need to know our token
TOKEN = 'insert-your-token-from-deverloper.ciscospark.com-here'
NAME =  'event-room-name-inserted-here'
RESTCONF = 'insert-restconf-ip-or-url-here'
APIC_EM = 'insert-apic-em-ip-or-url-here'


#Function to check if restconf is accessible
def check_restconf(address):
    # Retconf enabled device's address and default entry level
    restconf_api= "http://"+address+":9443/api"

    # Parameter passed during the call
    params = {"verbose" : ""}

    # Necessary headers to make an API call
    headers = {
        "authorization" : "Basic cm9vdDpDIXNjMDEyMw==",
        "content-type" : "application/vnd.yang.data+json",
        "accept" : "application/vnd.yang.api+json"
    }

    #Making Rest
    restconf_response = requests.get(restconf_api, headers=headers, params=params, verify=False)

    if restconf_response.ok:
        return True
    else:
        return False

#Function to check if apic-em is accessible
def check_apic_em(address):
    # Retconf enabled device's address and default entry level
    apic_em_api= "https://"+address+"/api/v1/ticket"

    # Necessary headers to make an API call
    headers = {
        "content-type": "application/json"
    }
    payload = {
        "username" : "devnetuser",
        "password" : "Cisco123!"
    }
    #Making Rest call
    apic_em_response = requests.post(apic_em_api, headers=headers, data=json.dumps(payload), verify=False)

    if apic_em_response.ok:
        return True
    else:
        return False



# this is the variable of the room id we need to figure out:
room_id = None
# you can replace room ID from output of script here
# room_id = 'your-room-id-output-from-the-script'


if not room_id:
    room_id = spark_get_room_id(TOKEN, NAME)


if room_id:
    spark_send_message(TOKEN, room_id, 'Hello room! My script verified that I can post messages to Spark using REST API calls.\n')
    if check_restconf(RESTCONF):
        spark_send_message(TOKEN, room_id, 'It also verified that RESTCONF enabled device is working properly.\n')
    else:
        spark_send_message(TOKEN, room_id, 'Unfortunately, RESTCONF enabled device is not working properly.\n')
    if check_apic_em(APIC_EM):
        spark_send_message(TOKEN, room_id, 'It also verified that APIC-EM is working properly.\n')
    else:
        spark_send_message(TOKEN, room_id, 'Unfortunately, APIC-EM is working properly.\n')
    print("Please check room " + NAME + ", there are messages posted on your behlaf")

