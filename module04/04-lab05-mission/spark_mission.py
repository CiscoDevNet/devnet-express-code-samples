import json
import sys
import requests

#MISSION: FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN 	= None #Replace None with your access token. Shroud with quotes.
ROOM_NAME		= None #Replace None with the name of the room to be created. Shroud with quotes.
YOUR_MESSAGE 	= None #Replace None with the message that you will post to the room. Shroud with quotes.


#sets the header to be used for authentication and data format to be sent.
def setHeaders():
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return (spark_header)


# creates a new room and returns the room id.
def createRoom(the_header,room_name):
	roomInfo = {"title":room_name}
	uri = 'https://api.ciscospark.com/v1/rooms'
	rooms = requests.get(uri, json=roomInfo, headers=the_header)
	for room in rooms.json()['items']:
		if room['title'] == room_name:
			print('Hi! That room already exists, so you do not need to create it.')
			print('Try using a different string for ROOM_NAME to see how to create a Spark room in python.')
			sys.exit()
	resp = requests.post(uri, json=roomInfo, headers=the_header)
	var = resp.json()
	print("createRoom JSON: ", var)
	#MISSION: REPLACE None WITH CODE THAT PARSES AND RETURNS THE ROOM ID.
	return(None)

# adds a new member to the room.  Member e-mail is test@test.com
def addMembers(the_header,roomId):
	member = {"roomId":roomId,"personEmail": "test@test.com", "isModerator": False}
	uri = 'https://api.ciscospark.com/v1/memberships'
	resp = requests.post(uri, json=member, headers=the_header)
	print("addMembers JSON: ", resp.json())

#posts a message to the room
def postMsg(the_header,roomId,message):
	message = {"roomId":roomId,"text":message}
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, json=message, headers=the_header)
	print("postMsg JSON: ", resp.json())

#MISSION: WRITE CODE TO RETRIEVE AND DISPLAY DETAILS ABOUT THE ROOM.
def getRoomInfo(the_header,roomId):
	print("In function getRoomInfo")
	#MISSION: Replace None in the uri variable with the Spark REST API call
	uri = None
	if uri == None:
		sys.exit("Please add the uri call to get room details.  See the Spark API Ref Guide")
	resp = requests.get(uri, headers=the_header)
	print("Room Info: ",resp.text)
	resp = resp.json()
	print("MISSION: Please add code to parse and display details about the room.")


if __name__ == '__main__':
	if ACCESS_TOKEN==None or ROOM_NAME==None or YOUR_MESSAGE==None:
		sys.exit("Please check that variables ACCESS_TOKEN, ROOM_NAME and YOUR_MESSAGE have values assigned.")
	header=setHeaders()
	#passing the ROOM_NAME for the room to be created
	room_id=createRoom(header,ROOM_NAME)
	if room_id == None:
		sys.exit("Please check that function createRoom returns the room ID value.")
	#passing roomId to members function here to add member to the room.
	addMembers(header,room_id)
	#passing roomId to message function here to Post Message to a room.
	postMsg(header,room_id,YOUR_MESSAGE)
	#MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)
	print("MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)")
