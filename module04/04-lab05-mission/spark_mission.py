#!/usr/bin/env python
import requests
import sys


# MISSION: FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN 	= None  # Replace None with your access token. Shroud with quotes.
ROOM_NAME		= None  # Replace None with the name of the room to be created. Shroud with quotes.
YOUR_MESSAGE 	= None  # Replace None with the message that you will post to the room. Shroud with quotes.


# sets the header to be used for authentication and data format to be sent.
def setHeaders():
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return (spark_header)


def rooms(the_header):
	uri = 'https://api.ciscospark.com/v1/rooms'
	data = requests.get(uri, headers=the_header)
	return(data.json()["items"])


# creates a new room and returns the room id.
def createRoom(the_header,room_name):
	roomInfo = {"title": room_name}
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.post(uri, json=roomInfo, headers=the_header)
	var = resp.json()
	print("createRoom JSON: ", var)
	# MISSION: REPLACE None WITH CODE THAT PARSES AND RETURNS THE ROOM ID.
	return(None)


# adds a new member to the room.  Member e-mail is test@test.com
def addMembers(the_header,roomId):
	member = {"roomId":roomId,"personEmail": "test@test.com", "isModerator": False}
	uri = 'https://api.ciscospark.com/v1/memberships'
	resp = requests.post(uri, json=member, headers=the_header)
	print("addMembers JSON: ", resp.json())

# posts a message to the room
def postMsg(the_header, roomId, message):
	message = {"roomId": roomId, "text": message}
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, json=message, headers=the_header)
	print("postMsg JSON: ", resp.json())


# MISSION: WRITE CODE TO RETRIEVE AND DISPLAY DETAILS ABOUT THE ROOM.
def getRoomInfo(the_header, roomId):
	print("In function getRoomInfo")
	# MISSION: Replace None in the uri variable with the Spark REST API call
	uri = None
	if uri is None:
		sys.exit("Please add the uri call to get room details.  See the Spark API Ref Guide.")
	resp = requests.get(uri, headers=the_header)
	print("Room Info: ", resp.text)
	resp = resp.json()
	print("MISSION: Please add code to parse and display details about the room.")


if __name__ == '__main__':
	if ACCESS_TOKEN is None or ROOM_NAME is None or YOUR_MESSAGE is None:
		sys.exit("Please check that variables ACCESS_TOKEN, ROOM_NAME and YOUR_MESSAGE have values assigned.")
	header = setHeaders()
	my_rooms = rooms(header)
	room_names = [room["title"] for room in my_rooms]
	room_id = None
	if ROOM_NAME not in room_names:
		# passing the ROOM_NAME for the room to be created
		print("Awesome! We are creating a new spark room named: {r}".format(r=ROOM_NAME))
		room_id = createRoom(header, ROOM_NAME)
	else:
		for room in my_rooms:
			if room["title"] == ROOM_NAME:
				print("Cool! We found an existing room named: {r}".format(r=ROOM_NAME))
				print("We'll post our messages to this room!")
				room_id = room["id"]

	if room_id is None:
		sys.exit("Please check that function createRoom returns the room ID value.")
    # passing roomId to members function here to add member to the room.
	addMembers(header, room_id)
	# passing roomId to message function here to Post Message to a room.
	postMsg(header, room_id, YOUR_MESSAGE)
	# MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)
	print("MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)")
