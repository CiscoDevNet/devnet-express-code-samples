#!/usr/bin/env python
# ############################################################################
# Copyright (c) 2016 Bruno Klauser <bklauser@cisco.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ''AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#
# TECHNICAL ASSISTANCE CENTER (TAC) SUPPORT IS NOT AVAILABLE FOR THIS SCRIPT.
#
# Always check for the latest Version of this script via http://cs.co/NWPLab
# ############################################################################
#
# This script contains a set of shared environment definitions
#
# ############################################################################
import base64
import json
import requests
import sys
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass

# Replace YOUR-NAME-HERE in the line below
LAB_USER = '<YOUR-NAME-HERE>'

# Get your Cisco Spark access token from developer.ciscospark.com
# 1) Login
# 2) Copy the Access Token from top-right corner portrait icon
# 3) replace YOUR-ACCESS-TOKEN-HERE in the line below
LAB_USER_SPARK_TOKEN = '<YOUR-ACCESS-TOKEN-HERE>'

# ############################################################################
# Do not edit below this line, unless instructed to do so
# ############################################################################
LAB_SESSION = 'dCloud DNA Enterprise Network Programmability Lab v1.2'

SPARK_ROOM_NAME = 'dCloud DNA Enterprise Network Programmability Lab v1.2'
SPARK_TOKEN = 'Bearer ' + LAB_USER_SPARK_TOKEN
SPARK_HEADERS = {
    'Content-type': 'application/json',
    'Authorization': SPARK_TOKEN
}
SPARK_API = 'https://api.ciscospark.com/v1'
SPARK_API_MESSAGES = '%s/messages' % SPARK_API
SPARK_API_ROOMS = '%s/rooms' % SPARK_API


APIC_EM_USR = 'devnetuser'
APIC_EM_PWD = 'Cisco123!'
APIC_EM_HOST = 'sandboxapic.cisco.com'
APIC_EM_API = 'https://%s/api/v1' % APIC_EM_HOST


RESTCONF_USR = 'root'
RESTCONF_PWD = 'C!sc0123'
RESTCONF_URL = 'https://devnetapi.cisco.com/sandbox/restconf/api/running/native/hostname'
# Note: the below is to accommodate different syntax in Python 2 vs 3:
try:
    RESTCONF_CREDENTIALS = bytes(RESTCONF_USR + ':' + RESTCONF_PWD)
except Exception:
    RESTCONF_CREDENTIALS = bytes(RESTCONF_USR + ':' + RESTCONF_PWD, 'utf-8')

RESTCONF_B64 = (base64.b64encode(RESTCONF_CREDENTIALS)).decode('utf-8')
RESTCONF_HEADERS = {
    'authorization': "Basic " + RESTCONF_B64,
    'content-type': "application/vnd.yang.data+json",
    'accept': "application/vnd.yang.data+json"
}


# ############################################################################
# Utiliy Function to find and post a message into SPARK_ROOM_NAME
# ############################################################################
def postSparkMessage(tmp_message):
    global SPARK_ROOM_ID
    SPARK_ROOM_ID = None
    r = requests.get(SPARK_API_ROOMS, headers=SPARK_HEADERS, verify=False)
    j = json.loads(r.text)

    for tmproom in j['items']:
        if tmproom['title'] == SPARK_ROOM_NAME:
            SPARK_ROOM_ID = tmproom['id']
            print("Found room ID for '" + SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
            break

    if SPARK_ROOM_ID is None:
        print("Failed to find room ID for '" + SPARK_ROOM_NAME + "'")
        return None
    else:
        m = json.dumps({'roomId': SPARK_ROOM_ID, 'text': tmp_message})
        r = requests.post(SPARK_API_MESSAGES, data=m, headers=SPARK_HEADERS, verify=False)
        return r

# ############################################################################
# EOF
# ############################################################################
