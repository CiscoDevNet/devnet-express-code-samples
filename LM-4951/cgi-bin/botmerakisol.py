#!/usr/local/bin/python3

import pyCiscoSpark as Spark
import sys
import json
import os
import logging
import requests
from logging.handlers import RotatingFileHandler
from logging import Formatter

global data

meraki_key = "7352ee8d5dcfbb0967d6a2366ed1d4e33af23468" #+ "!" #comment to enable Meraki API

print("Content-type:text/html\r\n\r\n")
print("here")

def parse_data(data):
    dataDict = data
    log.info(data)
    decode_msg(dataDict['data']['id'])


def decode_msg(msgId):
    uri = 'https://api.ciscospark.com/v1/messages/' + msgId
    resp = Spark.get_message(accessToken, msgId)
    log.info(resp)
    if resp['personId'] != 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS8wNWUwOGRlOC0zYjE3LTQyZjQtYjM3Zi1iMzNmMjg4ZWM1OTA':  # Bot ID prevents infinit loop
        log.info("doing something")
        do_something(resp)


def do_something(resp):
    trig = resp['text'].split()
    log.info(trig[0])
    if trig[0].lower() in ['webhook', 'webhooks', 'hook', 'hooks']:
        do_spark(resp)
    elif trig[0].lower() == 'meraki':
        do_meraki(resp)
    else:
        Spark.post_message(accessToken, resp['roomId'], resp['text'])  # echo


def do_spark(resp):
    md = json.dumps(data, indent=4, separators=(',', ': '))
    Spark.post_markdown(accessToken, resp['roomId'], md)


def do_meraki(resp):
    # Create a list of incoming text
    trig = resp['text'].split()

    # Content type and Authorization information must be included in the header
    header = {"content-type": "application/json", "X-Cisco-Meraki-API-Key": meraki_key}
    endpoint = ''
    keyword = ''

    # Meraki API resources
    baseURL = 'https://n149.meraki.com/api/v0'

    if trig[1].lower() in ['organization', 'organizations', 'org', 'orgs']:
        keyword = 'org'
        endpoint = '/organizations'
    elif trig[1].lower() in ['networks', 'network', 'net']:
        if len(trig) > 2:
            keyword = 'net'
            endpoint = '/organizations/' + trig[2] + '/networks'
        else:
            Spark.post_markdown(accessToken, resp['roomId'], 'Please provide Org ID **/meraki Network [orgID]**')
    elif trig[1].lower() in ['device', 'devices']:
        if len(trig) > 2:
            keyword = 'dev'
            endpoint = '/networks/' + trig[2].upper() + '/devices'  # /networks/[networkId]/devices
            log.info(endpoint)
        else:
            Spark.post_markdown(accessToken, resp['roomId'],
                                'Please provide Network ID **/meraki Devices [networkID]**')
    elif trig[1].lower() in ['switch', 'switchport', 'switches']:
        if len(trig) > 2:
            keyword = 'sw'
            endpoint = '/devices/' + trig[2].upper() + '/switchPorts'  # /devices/[serial]/switchPorts
            log.info(endpoint)
        else:
            Spark.post_markdown(accessToken, resp['roomId'],
                                'Please provide Switch SerialNum **/meraki switch [SerialNum]**')
    elif trig[1].lower() in ['clients', 'client']:
        if len(trig) > 2:
            keyword = 'cli'
            endpoint = '/devices/' + trig[2].upper() + '/clients?timespan=86400'  # /devices/[serial]/switchPorts
            log.info(endpoint)
        else:
            Spark.post_markdown(accessToken, resp['roomId'],
                                'Please provide Device SerialNum **/meraki client [SerialNum]**')
    elif trig[1].lower() in ['admin', 'admins']:
        resp['text'] = clean_text(resp['text'])
        if len(trig) > 2:
                keyword = 'admin'
                endpoint = "/organizations/" + trig[2].upper() + "/admins"
        else:
            Spark.post_markdown(accessToken, resp['roomId'],'Please provide Org ID **/meraki Admin [orgID]**')
    elif trig[1].lower() in ['addadmin']:
        if len(trig) > 2:
            org = trig[2]
            user = '{"name": "' + trig[4] + ' ' + trig[5] + '", "email": "' + trig[7] + '", "orgAccess": "full", "tags": []}'
            user = {}
            user["name"] =  trig[4] + ' ' + trig[5]
            user["email"] = trig[7]
            user["orgAccess"] = "full"
            user["tags"] = []
            code = add_user(org, user, header)
            log.info(type(resp))
            if code == 201:
                Spark.post_markdown(accessToken, resp['roomId'], '**' + user["name"] + '** has been granted full Access')
            else:
                Spark.post_markdown(accessToken, resp['roomId'], '**Error ** ' + code)
        else:
            Spark.post_markdown(accessToken, resp['roomId'], 'Please provide Org ID **/meraki AddAdmin [orgID]**')

    elif trig[1].lower() in ['removeadmin']:
        if len(trig) > 2:
            org = trig[2]
            userid = trig[4]
            remove_user(org,userid,header)
        else:
            Spark.post_markdown(accessToken, resp['roomId'], 'Please provide Org ID **/meraki RemoveAdmin [orgID]**')


    # Performs a GET on the specified url to get the service ticket
    log.info(baseURL + endpoint)
    response = requests.get(baseURL+endpoint, headers=header)
    log.info(response)
    log.info(response.json())
    md = send_meraki(response, keyword)
    Spark.post_markdown(accessToken, resp['roomId'], md)


def send_meraki(resp, kw):
    md = ''
    hdr = ''
    if kw == 'org':
        hdr = '- **Org Id | Name** \n'
    elif kw == 'net':
        hdr = '- **Network ID | OrgId | Type | Name** \n'
    elif kw == 'dev':
        hdr = '- **Name | Mac | Model | Serial** \n'
    elif kw == 'sw':
        hdr = '- **Number | Type | vlan | poeEnabled | enabled** \n'
    elif kw == 'cli':
        hdr = '- **ip | mac | Dns Name | description** \n'
    elif kw == 'admin':
        hdr = '- **Name | Email | Org Access | id** \n'

    #Parse JSON coming back from Meraki API
    for meraki_payload in resp.json():
        if kw == 'org':
            md = md + '- ' + \
                 str(meraki_payload['id']) + ' | ' + \
                 str(meraki_payload['name']) + '\n'
        elif kw == 'net':
            md = md + '- ' + \
                 str(meraki_payload['id']) + ' | ' + \
                 str(meraki_payload['organizationId']) + ' | ' + \
                 str(meraki_payload['type']) + ' | ' + \
                 str(meraki_payload['name']) + '\n'
        elif kw == 'dev':
            md = md + '- ' + \
                 str(meraki_payload['name']) + ' | ' +\
                 str(meraki_payload['mac']) + ' | ' + \
                 str(meraki_payload['model']) + ' | ' + \
                 str(meraki_payload['serial']) + '\n'
        elif kw == 'sw':
            md = md + '- ' + \
                 str(meraki_payload['number']) + ' | ' +\
                 str(meraki_payload['type']) + ' | ' + \
                 str(meraki_payload['vlan']) + ' | ' + \
                 str(meraki_payload['poeEnabled']) + ' | ' + \
                 str(meraki_payload['enabled']) + '\n'
        elif kw == 'cli':
            md = md + '- ' + \
                 str(meraki_payload['ip']) + ' | ' +\
                 str(meraki_payload['mac']) + ' | ' + \
                 str(meraki_payload['mdnsName']) + ' | ' + \
                 str(meraki_payload['description']) + ' | ' + '\n'
        elif kw == 'admin':
            md = md + '- ' + \
                 str(meraki_payload['name']) + ' | ' +\
                 str(meraki_payload['email']) + ' | ' + \
                 str(meraki_payload['orgAccess']) + ' | ' + \
                 str(meraki_payload['id']) + ' | ' + '\n'
    return hdr + md


def add_user(org, user, header):
    payload = {"name": user["name"], "email": user["email"], "orgAccess": "full", "tags": []}
    url = "https://n149.meraki.com/api/v0/organizations/" + str(org) + "/admins"
    log.info(type(user))
    post_resp = requests.post(url, data=json.dumps(user), headers=header)
    log.info(post_resp.status_code)
    if post_resp.status_code == 201:
        return 201
    else:
        error = str(post_resp.content)
        return error


def remove_user(org, userid_to_remove, header):
    url = "https://n149.meraki.com/api/v0/organizations/" + str(org) + "/admins/" + str(userid_to_remove)
    print(url)
    del_resp = requests.delete(url, headers=header)
    log.info(del_resp.status_code)

def clean_text(txt):
    txt = txt.lower()
    txt = txt.replace("meraki ", "")
    txt = txt.replace("?","")
    txt = txt.replace("/", "")
    txt = txt.replace("!", "")
    return txt


def log_file():
    global curDir
    global log
    curDir = os.path.dirname(os.path.abspath(__file__))
    log = logging.getLogger('rotating log')
    log.setLevel(logging.INFO)
    handler = RotatingFileHandler(curDir + '/debug_rooms.log', maxBytes=1048576, backupCount=10)
    handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(message)s'))
    log.addHandler(handler)


if __name__ == '__main__':
    log_file()
    accessToken = 'ZTE0N2NmMTMtY2Y1Ni00N2U5LWE0MWEtYTNiOTM2NGNiNzYwM2Y0M2Y3YmMtMjIw'
    #accessToken = Spark.get_token()
    log.info('starting read of specific length')
    data = sys.stdin.read(int(os.environ.get('CONTENT_LENGTH', 0)))
    log.info('ending read')
    data = json.loads(data)
    parse_data(data)
