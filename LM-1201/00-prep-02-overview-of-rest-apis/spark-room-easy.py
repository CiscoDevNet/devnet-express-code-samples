import json
import requests

accessToken = "" #put your access token between the quotes.


accessToken_hdr = 'Bearer ' + accessToken
webex_header = {'Authorization': accessToken_hdr}
uri = 'https://api.ciscospark.com/v1/rooms'
resp = requests.get(uri, headers=webex_header)
print("Webex Teams rooms you belong to: ")	
print(resp.text)

print()
print("Webex Teams rooms in easier to read format - pretty format:")
print (json.dumps(resp.json(), indent=4, separators=(',', ': ')))

