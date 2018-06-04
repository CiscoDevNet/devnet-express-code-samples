#!/usr/bin/env python

import requests


def _headers(token):
    """
    builds the needed HTTP headers for Webex Teams
    In:
        token: Webex Teams Auth Token (str)
    Out:
        HTTP Header (dict)
    """
    return {'Content-type': 'application/json',
            'Authorization': 'Bearer ' + token}


def _webex_teams_api(noun):
    """
    returns the proper Webex Teams URI based on the given noun
    In:
        noun: Webex Teams noun (rooms, messages, ...), (str)
    Out:
        URL (str)
    """
    return ''.join(('https://api.ciscospark.com/v1/', noun))


def webex_teams_get_room_id(token, name):
    """
    returns the Webex Teams room Id for the given room name
    In:
        token: Webex Teams auth token (str)
        name: Webex Teams room name (str)
    Out:
        Webex Teams room Id (str) or None if not found
    """
    query = {'type': 'group', 'max': 1000}
    uri = _webex_teams_api('rooms')

    while uri:
        r = requests.get(uri, params=query, headers=_headers(token))
        if r.ok:
            # go through all rooms, return room_id, if found
            for room in r.json().get('items'):
                if room['title'] == name:
                    return room['id']
            # not found, do we have more rooms to load?
            uri = r.links.get('next')
            if uri:
                uri = uri.get('url', None)
        else:
            print('Reponse from Webex Teams: ' + str(r.status_code))
            print('Your connection to Webex Teams failed. Check the Webex Teams Authorization Token.')
            uri = None
    return None


def webex_teams_send_message(token, room_id, msg):
    """
    sends a message msg to the given room Id, using the Webex Teams token
    In:
        token: Webex Teams auth token (str)
        room_id: Webex Teams room Id, must exist (str)
        msg: Message that should be posted (str)
    Out:
        success (bool)
    """
    m = {'roomId': room_id, 'text': msg}
    r = requests.post(_webex_teams_api('messages'), json=m, headers=_headers(token))
    return r.ok
