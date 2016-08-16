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
# This sample script illustrates how to run a Path Trace in APIC-EM via it's
# REST APIs. This includes
# 1) posting a path trace request
# 2) querying and parsing the resulting path trace JSON document
# 3) extracting host names and posting them into Spark
# 
# ############################################################################
import _LabEnv
from pprint import pprint
from pprint import pformat
import io
import time
import json
import requests
# Disable Certificate warning
try:
  requests.packages.urllib3.disable_warnings()
except:
  pass

##############################################################################
# Variables below
##############################################################################
PATH_SOURCE_IP = '65.1.1.46'
PATH_DEST_IP = '212.1.10.20'

# ############################################################################
# Start API Session
# ############################################################################
apic_credentials = json.dumps({'username':_LabEnv.APIC_EM_USR,'password':_LabEnv.APIC_EM_PWD})
tmp_headers = {'Content-type': 'application/json'}
tmp_post = '%s/ticket' % _LabEnv.APIC_EM_API
r = requests.post(tmp_post, data=apic_credentials, verify=False, headers=tmp_headers)
print('APIC-EM Response: ' + r.text)

# Add session ticket to my http header for subsequent calls
apic_session_ticket = r.json()['response']['serviceTicket']
APIC_EM_HEADERS = {'Content-type': 'application/json', "X-Auth-Token": apic_session_ticket}

##############################################################################
# Post a Network Path Trace Request
##############################################################################
tmp_post = '%s/flow-analysis' % _LabEnv.APIC_EM_API
tmp_data = tmp_data = json.dumps({'sourceIP':PATH_SOURCE_IP,'destIP':PATH_DEST_IP})
print('My POST Request: ' + tmp_post + tmp_data)
req = requests.post(tmp_post, data=tmp_data, verify=False, headers=APIC_EM_HEADERS)

my_parsed_response = req.json()
print('Parsed JSON Response: ')
pprint(my_parsed_response)

my_flow_id = my_parsed_response['response']['flowAnalysisId']
print('Flow Analysis ID: ' + my_flow_id)

##############################################################################
# Query the resulting Path
##############################################################################
# Better practice: poll for existence of endTime attribute in task
print('Lets give APIC-EM a few seconds to complete the trace ...')
time.sleep(15)

tmp_get = _LabEnv.APIC_EM_API + '/flow-analysis/' + my_flow_id
print('My GET Request: ' + tmp_get)
req = requests.get(tmp_get, verify=False, headers=APIC_EM_HEADERS)

# Printing result using a few different methods
my_parsed_response = req.json()
print('Parsed JSON Response - full: ')
pprint(my_parsed_response)

print('Parsed JSON Response - subset Python Dict object: ')
my_nodes_on_path = my_parsed_response['response']['networkElementsInfo']

my_nodes = []
for p in my_nodes_on_path:
  my_nodes.append( p.get('name', '.') ) 
  my_nodes.append( " " )
my_path = ''.join(my_nodes)
print('Hostnames on the path from %s to %s are: \n %s' % (PATH_SOURCE_IP, PATH_DEST_IP, my_path) )

# ############################################################################
# Post to Spark
# ############################################################################
tmp_text = 'Hello '+ _LabEnv.LAB_SESSION +', nodes from '+ PATH_SOURCE_IP +' to '+ PATH_DEST_IP +' are: \n' + my_path
r = _LabEnv.postSparkMessage(tmp_text)
print('Spark Response: ' + r.text)

##############################################################################
# EOF
##############################################################################
