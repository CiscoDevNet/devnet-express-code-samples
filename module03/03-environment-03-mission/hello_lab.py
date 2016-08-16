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
# This is a simple hello lab script (will create the spark room if needed)
#
# ############################################################################
import json
import lab_env
import requests
import sys
# Disable Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass

# ############################################################################
# Variables below
# ############################################################################
SPARK_ROOM_ID = None

# ############################################################################
# Find (or Create) Spark Room
# ############################################################################
r = requests.get(lab_env.SPARK_API_ROOMS, headers=lab_env.SPARK_HEADERS, verify=False)
j = json.loads(r.text)

for tmproom in j['items']:
    if tmproom['title'] == lab_env.SPARK_ROOM_NAME:
        SPARK_ROOM_ID = tmproom['id']
        print("Found room ID for '" + lab_env.SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
        break

if SPARK_ROOM_ID is None:
    print("Failed to find room ID for '" + lab_env.SPARK_ROOM_NAME + " creating it ...'")
    t = json.dumps({'title': lab_env.SPARK_ROOM_NAME})
    # print('Spark Request: ' + t)
    r = requests.post(lab_env.SPARK_API_ROOMS, data=t, headers=lab_env.SPARK_HEADERS, verify=False)
    # print('Spark Response: ' + r.text)
    j = json.loads(r.text)
    SPARK_ROOM_ID = j['id']

if SPARK_ROOM_ID is None:
    print("Failed to find or create room ID for '" + lab_env.SPARK_ROOM_NAME + "'")
    sys.exit(1)

# ############################################################################
# Verify Lab Environment
# ############################################################################

ucgood = '\u2705'
ucbad = '\u274C'

# Python Version and Platform info
labstate = ucgood + ' Python (' + sys.version + ' on ' + sys.platform + ')\n'

# Spark Room info
labstate = labstate + ucgood + ' Spark Room (ID=' + SPARK_ROOM_ID + ')\n'

# dCloud Session info
# TBD once session.xml is provisioned
# dCloudSession = '000000'
# dCloudDC = 'N/A'
# dCloudPOD = 'POD %s (%s)' % (dCloudSession, dCloudDC)

# APIC-EM info
apic_credentials = json.dumps({'username': lab_env.APIC_EM_USR, 'password': lab_env.APIC_EM_PWD})
tmp_headers = {'Content-type': 'application/json'}
tmp_post = '%s/ticket' % lab_env.APIC_EM_API
try:
    r = requests.post(tmp_post, data=apic_credentials, verify=False, headers=tmp_headers)
    ticket = r.json()['response']['serviceTicket']
except Exception:
    ticket = None
# labstate = labstate + ucgood + ' APIC-EM Login '+ str(r.json()['response']) +')\n'

# RESTCONF info
try:
    r = requests.get(lab_env.RESTCONF_URL, auth=(lab_env.RESTCONF_USR, lab_env.RESTCONF_PWD), headers=lab_env.RESTCONF_HEADERS, verify=False)
    hostname = r.json()['ned:hostname']
except Exception:
    hostname = None

# CSR1000 info
# TBD

# N9000 info
# TBD

# VIRL info
# TBD

# vNAM info
# TBD


# ############################################################################
# Post into Spark Room
# ############################################################################
messagetext = 'Hello %s this is %s \n' % (lab_env.LAB_SESSION, lab_env.LAB_USER)
r = lab_env.postSparkMessage(messagetext)
if ticket is not None:
    r = lab_env.postSparkMessage('We were able to reach the APIC-EM controller!')
else:
    r = lab_env.postSparkMessage('Uh oh! We had issues reaching the APIC-EM controller! Try checking your lab setup.')

if hostname is not None:
    r = lab_env.postSparkMessage('We were able to reach the CSR1000V using RESTCONF!')
else:
    r = lab_env.postSparkMessage('Uh oh! We had issues reaching the CSR1000V using RESTCONF! Try checking your lab setup.')


# ############################################################################
# EOF
# ############################################################################
