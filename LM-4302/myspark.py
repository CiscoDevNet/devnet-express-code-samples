#!/usr/bin/env python

import requests


def _headers(token):
    """
    builds the needed HTTP headers for Spark
    In:
        token: Spark Auth Token (str)
    Out:
        HTTP Header (dict)
    """
    return {'Content-type': 'application/json',
            'Authorization': 'Bearer ' + token}


def _spark_api(noun):
    """
    returns the proper Spark URI based on the given noun
    In:
        noun: Spark noun (rooms, messages, ...), (str)
    Out:
        URL (str)
    """
    return ''.join(('https://api.ciscospark.com/v1/', noun))


def spark_get_room_id(token, name):
    """
    returns the Spark room Id for the given room name
    In:
        token: Spark auth token (str)
        name: Spark room name (str)
    Out:
        Spark room Id (str) or None if not found
    """
    query = {'type': 'group', 'max': 1000}
    uri = _spark_api('rooms')

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
            print('Reponse from Spark: ' + str(r.status_code))
            print('Your connection to Spark failed. Check the Spark Authorization Token.')
            uri = None
    return None


def spark_send_message(token, room_id, msg):
    """
    sends a message msg to the given room Id, using the Spark token
    In:
        token: Spark auth token (str)
        room_id: Spark room Id, must exist (str)
        msg: Message that should be posted (str)
    Out:
        success (bool)
    """
    m = {'roomId': room_id, 'text': msg}
    r = requests.post(_spark_api('messages'), json=m, headers=_headers(token))
    return r.ok
