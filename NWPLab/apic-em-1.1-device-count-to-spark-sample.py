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
# This sample script illustrates how to 
# 1) query the number of network devices from the APIC-EM network information 
#    base via the APIC-EM REST APIs and
# 2) post the result into Spark using a predefined function in _LabEnv
# 
# ############################################################################
import _LabEnv
from pprint import pprint
import json
import requests
# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

# ############################################################################
# Start API Session
# ############################################################################
apic_credentials = json.dumps({'username':_LabEnv.APIC_EM_USR,'password':_LabEnv.APIC_EM_PWD})
tmp_headers = {'Content-type': 'application/json'}
tmp_post = '%s/ticket' % _LabEnv.APIC_EM_API
print('My POST Request: ' + tmp_post)
r = requests.post(tmp_post, data=apic_credentials, verify=False, headers=tmp_headers)
print('APIC-EM Response: ' + r.text)
print('APIC-EM Session Ticket: ' + r.json()['response']['serviceTicket'])
print('APIC-EM Session Timeout: ' + str(r.json()['response']['sessionTimeout']))
print('APIC-EM Idle Timeout: ' + str(r.json()['response']['idleTimeout']))

# Add session ticket to my http header for subsequent calls
apic_session_ticket = r.json()['response']['serviceTicket']
APIC_EM_HEADERS = {'Content-type': 'application/json', "X-Auth-Token": apic_session_ticket}

# ############################################################################
# Get Network Device Count
# ############################################################################
tmp_get = '%s/network-device/count' % _LabEnv.APIC_EM_API
print('My GET Request: ' + tmp_get)
r = requests.get(tmp_get, verify=False, headers=APIC_EM_HEADERS)
print('APIC-EM Response: ' + r.text)

my_parsed_response = r.json()
print('Parsed JSON Response: ')
pprint(my_parsed_response)

my_device_count = my_parsed_response['response']
print('Network Device Count: ' + str(my_device_count))

# ############################################################################
# Share the News
# ############################################################################
tmp_text = 'Hello ' + _LabEnv.LAB_SESSION + ', my APIC-EM at manages '  + str(my_device_count) + ' Devices.'
r = _LabEnv.postSparkMessage(tmp_text)
print('Spark Response: ' + r.text)

# ############################################################################
# EOF
# ############################################################################
