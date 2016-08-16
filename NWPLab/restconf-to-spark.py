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
# This sample script illustrates how to query operational data from a router 
# via the RESTCONF API and then post the results into an existing Spark room 
# via the Spark REST APIs.
# 
# Initial Version by Joe Clarke - thanks Joe!
# ############################################################################
import _LabEnv
import requests
import json
import sys

# ############################################################################
# Variables below
# ############################################################################
RESTCONF_API  = "http://198.18.133.218:8008/api/operational/interfaces-state?deep"
INTF      = 'GigabitEthernet1'
TEXT      = 'Hello, %s, this is %s.  Interface %s has received %d bytes and transmitted %d bytes.'
SPARK_ROOM_ID = None

# ############################################################################
# Get Router Interface Data via RESTCONF
# ############################################################################
response = requests.request("GET", RESTCONF_API, headers=_LabEnv.RESTCONF_HEADERS, verify=False)
j = json.loads(response.text)
in_octets = -1
out_octets = -1
for intf in j['ietf-interfaces:interfaces-state']['interface']:
    if intf['name'] == INTF:
        in_octets = intf['statistics']['in-octets']
        out_octets = intf['statistics']['out-octets']
        break
if in_octets == -1 or out_octets == -1:
    print("Failed to find statistics for interface " + INTF)
    sys.exit(1)
   
# ############################################################################
# Post to Spark Room
# ############################################################################
messagetext = TEXT % (_LabEnv.LAB_SESSION, _LabEnv.LAB_USER, INTF, in_octets, out_octets)
r = _LabEnv.postSparkMessage(messagetext)
print('Spark Response: ' + r.text)

# ############################################################################
# EOF
# ############################################################################