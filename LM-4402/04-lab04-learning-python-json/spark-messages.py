import json
import requests

ACCESS_TOKEN = "" #put your access token between the quotes.
ROOM_NAME    = "" #put the name of a room to which you belong between the quotes.
MESSAGE      = "" #put your message between the quotes.


def setHeaders():         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return spark_header


def getRooms(theHeader):    
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.get(uri, headers=theHeader)	
	return resp.json()

def findRoom(roomList,name):
	roomId=0
	for room in roomList["items"]:	
		if room["title"] == name:
			roomId=room["id"]
			break
	return roomId

def getRoomMessages(theHeader,roomID):    
	uri = 'https://api.ciscospark.com/v1/messages?roomId=' + roomID
	resp = requests.get(uri, headers=theHeader)	
	return resp.json()
	
def addMessageToRoom(theHeader,roomID,message):
	uri = "https://api.ciscospark.com/v1/messages"
	payload= {"roomId":roomID,"text":message}
	resp = requests.post(uri, data=json.dumps(payload), headers=theHeader)	
	return resp.json()


header=setHeaders()
rooms=getRooms(header)
print("Rooms:")
print (json.dumps(rooms, indent=4, separators=(',', ': ')))
roomID=findRoom(rooms,ROOM_NAME)
if roomID != 0:
	msgList=getRoomMessages(header,roomID)
	print()
	print("Messages in " + ROOM_NAME)
	print (json.dumps(msgList, indent=4, separators=(',', ': ')))
	resp=addMessageToRoom(header,roomID,MESSAGE)
	print(resp)
	msgList=getRoomMessages(header,roomID)
	print("Messages in " + ROOM_NAME)
	print (json.dumps(msgList, indent=4, separators=(',', ': ')))
else:
	print("Specified room was not found!")
