#!/usr/bin/python3

import requests
import json
import ntpath
import re
from pymongo import MongoClient
from requests_toolbelt.multipart.encoder import MultipartEncoder


# COMMENTED SECTION BELOW FOR DEBUGGING

#import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
#try:
#    import http.client as http_client
#except ImportError:
    # Python 2
#    import httplib as http_client
#http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger('requests.packages.urllib3')
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True


# Helpers
def _url(path):
    return 'https://api.ciscospark.com/v1' + path


def _fix_at(at):
    at_prefix = 'Bearer '
    if not re.match(at_prefix, at):
        return 'Bearer ' + at
    else:
        return at


def findroomidbyname(at, roomname):
    room_dict = get_rooms(_fix_at(at))
    for room in room_dict['items']:
        # print (room['title'])
        if room['title'] == roomname:
            return room['id']
        else:
            return


# GET Requests
def get_token():
    client = MongoClient("mongodb://kiskander:peaceD00d@ds013162.mlab.com:13162/spark")
    db = client.get_default_database()
    spark = db['spark']
    query = {'username': 'DevNetBot'}
    cursor = spark.find(query)
    for doc in cursor:
        accessToken = doc['accessToken']
    return accessToken


def get_people(at, email='', displayname='', max=10):
    headers = {'Authorization': _fix_at(at)}
    payload = {'max': max}
    if email:
        payload['email'] = email
    if displayname:
        payload['displayName'] = displayname
    # print (payload)
    resp = requests.get(_url('/people'), params=payload, headers=headers)
    people_dict = json.loads(resp.text)
    people_dict['statuscode'] = str(resp.status_code)
    return people_dict


def get_persondetails(at, personId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/people/{:s}/'.format(personId)), headers=headers)
    person_detail_dict = json.loads(resp.text)
    person_detail_dict['statuscode'] = str(resp.status_code)
    return person_detail_dict


def get_me(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/people/me'), headers=headers)
    print(resp.text)
    me_dict = json.loads(resp.text)
    me_dict['statuscode'] = str(resp.status_code)
    return me_dict


def get_rooms(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/rooms'), headers=headers)
    room_dict = json.loads(resp.text)
    room_dict['statuscode'] = str(resp.status_code)
    return room_dict


def get_room(at, roomId):
    headers = {'Authorization': _fix_at(at)}
    payload = {'showSipAddress': 'true'}
    resp = requests.get(_url('/rooms/{:s}'.format(roomId)), params=payload, headers=headers)
    room_dict = json.loads(resp.text)
    room_dict['statuscode'] = str(resp.status_code)
    return room_dict


def get_memberships(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/memberships'), headers=headers)
    membership_dict = json.loads(resp.text)
    membership_dict['statuscode'] = str(resp.status_code)
    return membership_dict


def get_memberships_filtered(at,roomId):
    headers = {'Authorization': _fix_at(at)}
    filter_uri = '/memberships?roomId=' + roomId
    resp = requests.get(_url(filter_uri), headers=headers)
    membership_dict = json.loads(resp.text)
    membership_dict['statuscode'] = str(resp.status_code)
    return membership_dict


def get_membership(at, membershipId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/memberships/{:s}'.format(membershipId)), headers=headers)
    membership_dict = json.loads(resp.text)
    membership_dict['statuscode'] = str(resp.status_code)
    return membership_dict


def get_messages(at, roomId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId}
    resp = requests.get(_url('/messages'), params=payload, headers=headers)
    messages_dict = json.loads(resp.text)
    messages_dict['statuscode'] = str(resp.status_code)
    return messages_dict


def get_message(at, messageId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/messages/{:s}'.format(messageId)), headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    return message_dict


def get_webhooks(at):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/webhooks'), headers=headers)
    webhook_dict = json.loads(resp.text)
    webhook_dict['statuscode'] = str(resp.status_code)
    return webhook_dict


def get_webhook(at, webhookId):
    headers = {'Authorization': _fix_at(at)}
    resp = requests.get(_url('/webhooks/{:s}'.format(webhookId)), headers=headers)
    webhook_dict = json.loads(resp.text)
    webhook_dict['statuscode'] = str(resp.status_code)
    return webhook_dict


# POST Requests
def post_createroom(at, title):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'title': title}
    resp = requests.post(url=_url('/rooms'), json=payload, headers=headers)
    create_room_dict = json.loads(resp.text)
    create_room_dict['statuscode'] = str(resp.status_code)
    return create_room_dict


def post_message(at, roomId, text, toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'text': text}
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), data=json.dumps(payload), headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    return message_dict


def post_markdown(at, roomId, markdown, toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'markdown': markdown}
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), data=json.dumps(payload), headers=headers)
    message_dict = json.loads(resp.text)
    message_dict['statuscode'] = str(resp.status_code)
    return message_dict


def post_file(at, roomId, url, text='', toPersonId='', toPersonEmail=''):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'files': [url]}
    if text:
        payload['text'] = text
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    resp = requests.post(url=_url('/messages'), json=payload, headers=headers)
    file_dict = json.loads(resp.text)
    file_dict['statuscode'] = str(resp.status_code)
    return file_dict


def post_localfile(at, roomId, filename, text='', toPersonId='', toPersonEmail=''):
    openfile = open(filename, 'rb')
    filename = ntpath.basename(filename)
    payload = {'roomId': roomId, 'files': (filename, openfile, 'image/jpg')}
    if text:
        payload['text'] = text
    if toPersonId:
        payload['toPersonId'] = toPersonId
    if toPersonEmail:
        payload['toPersonEmail'] = toPersonEmail
    m = MultipartEncoder(fields=payload)
    headers = {'Authorization': _fix_at(at), 'Content-Type': m.content_type}
    resp = requests.request("POST",url=_url('/messages'), data=m, headers=headers)
    file_dict = json.loads(resp.text)
    file_dict['statuscode'] = str(resp.status_code)
    return file_dict


def post_membership(at, roomId, personEmail, isModerator=True):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'roomId': roomId, 'personEmail': personEmail, 'isModerator': isModerator}
    resp = requests.post(url=_url('/memberships'), json=payload, headers=headers)
    membership_dict = json.loads(resp.text)
    membership_dict['statuscode'] = str(resp.status_code)
    return membership_dict


def post_webhook(at, name, targetUrl, resource, event, filter):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name, 'targetUrl': targetUrl, 'resource': resource, 'event': event, 'filter': filter}
    resp = requests.post(url=_url('/webhooks'), json=payload, headers=headers)
    webhook_dict = json.loads(resp.text)
    webhook_dict['statuscode'] = str(resp.status_code)
    return webhook_dict


# PUTS
def put_room(at, roomId, title='title'):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'title': title}
    resp = requests.put(url=_url('/rooms/{:s}'.format(roomId)), json=payload, headers=headers)
    room_dict = json.loads(resp.text)
    room_dict['statuscode'] = str(resp.status_code)
    return room_dict


def put_membership(at, membershipId, isModerator):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'isModerator': isModerator}
    resp = requests.put(url=_url('/memberships/{:s}'.format(membershipId)), json=payload, headers=headers)
    membership_dict = json.loads(resp.text)
    membership_dict['statuscode'] = str(resp.status_code)
    return membership_dict


def put_webhook(at, webhookId, name, targetUrl):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    payload = {'name': name, 'targetUrl': targetUrl}
    resp = requests.put(url=_url('/webhooks/{:s}'.format(webhookId)),json=payload, headers=headers)
    webhook_dict = json.loads(resp.text)
    webhook_dict['statuscode'] = str(resp.status_code)
    return webhook_dict


# DELETES
def del_room(at, roomId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/rooms/{:s}'.format(roomId)), headers=headers)
    del_dict = {'statuscode': str(resp.status_code)}
    return del_dict


def del_membership(at, membershipId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/memberships/{:s}'.format(membershipId)), headers=headers)
    del_dict = {'statuscode': str(resp.status_code)}
    return del_dict


def del_message(at, messageId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/messages/{:s}'.format(messageId)), headers=headers)
    del_dict = {'statuscode': str(resp.status_code)}
    return del_dict


def del_webhook(at, webhookId):
    headers = {'Authorization': _fix_at(at), 'content-type': 'application/json'}
    resp = requests.delete(url=_url('/webhooks/{:s}'.format(webhookId)), headers=headers)
    del_dict = {'statuscode': str(resp.status_code)}
    return del_dict
