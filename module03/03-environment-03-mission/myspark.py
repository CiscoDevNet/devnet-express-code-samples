import json, requests

def _headers(token):
    return {'Content-type': 'application/json', 'Authorization': 'Bearer ' + token}


def _spark_api(noun):
    return ''.join(('https://api.ciscospark.com/v1/', noun))


def spark_get_room_id(token, name):
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
            uri = None
    return None

def spark_send_message(token, room_id, msg):
    m = json.dumps({'roomId': room_id, 'text': msg})
    requests.post(_spark_api('messages'), data=m, headers=_headers(token))
