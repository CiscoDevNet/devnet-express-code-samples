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
# This script illustrates how to find a spark room by name and post a message 
# 
# ############################################################################
import _LabEnv
import json
import requests
import sys

# ############################################################################
# Variables below
# ############################################################################
SPARK_ROOM_ID = None

# ############################################################################
# Find Room ID
# ############################################################################
r = requests.get(_LabEnv.SPARK_API_ROOMS, headers=_LabEnv.SPARK_HEADERS, verify=False)
j = json.loads(r.text)

for tmproom in j['items']:
  if tmproom['title'] == _LabEnv.SPARK_ROOM_NAME:
    SPARK_ROOM_ID = tmproom['id']
    print("Found room ID for '" + _LabEnv.SPARK_ROOM_NAME + "' : " + SPARK_ROOM_ID)
    break
    
if SPARK_ROOM_ID is None:
  print("Failed to find room ID for '" + _LabEnv.SPARK_ROOM_NAME + "'")
  sys.exit(1)

# ############################################################################
# Post to Spark Room
# ############################################################################
m = json.dumps({'roomId':SPARK_ROOM_ID,'text':'Full Hello '+_LabEnv.LAB_SESSION+' this is '+_LabEnv.LAB_USER})
r = requests.post(_LabEnv.SPARK_API_MESSAGES, data=m, headers=_LabEnv.SPARK_HEADERS, verify=False)
print('Spark Response: ' + r.text)

# ############################################################################
# EOF
# ############################################################################
