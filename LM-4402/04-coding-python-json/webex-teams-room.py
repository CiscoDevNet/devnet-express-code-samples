import json
import requests

accessToken = "" #put your access token here between the quotes.


def setHeaders():         
	accessToken_hdr = 'Bearer ' + accessToken
	webex_teams_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return webex_teams_header


def getRooms(theHeader):    
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.get(uri, headers=theHeader)	
	return resp.json()
    

header=setHeaders()
value=getRooms(header)
print (json.dumps(value, indent=4, separators=(',', ': ')))