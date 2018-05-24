import json
import requests

accessToken = "" #put your access token between the quotes.


accessToken_hdr = 'Bearer ' + accessToken
webex_teams_header = {'Authorization': accessToken_hdr}
uri = 'https://api.ciscospark.com/v1/rooms'
resp = requests.get(uri, headers=webex_teams_header)
print (json.dumps(resp.json(), indent=4, separators=(',', ': ')))
