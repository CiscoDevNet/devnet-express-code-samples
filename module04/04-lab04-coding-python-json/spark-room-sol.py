import json
import requests

accessToken = "NDQyZjU1NmQtMzc4Ni00YzA2LThkMzctNTE4ZGJmYTJlOThkY2IwMzVmMmEtOWM1" #put your access token here between the quotes.


def setHeaders():         
	accessToken_hdr = 'Bearer ' + accessToken
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return spark_header


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
print ("Spark Response Data:")
print (json.dumps(value, indent=4, separators=(',', ': ')))
parseData(value)