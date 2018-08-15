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

def parseData(data):
	for val in data["items"]:
		print()
		print("Room Name: " + val["title"])
		print("Last Active: " + val["lastActivity"])


header=setHeaders()
value=getRooms(header)
print ("Webex Teams Response Data:")
print (json.dumps(value, indent=4, separators=(',', ': ')))
parseData(value)