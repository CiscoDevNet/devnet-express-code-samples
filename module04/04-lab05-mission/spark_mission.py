import json
import sys
import requests

#MISSION: FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN = None #put your access token between the quotes
ROOM_NAME = None #give the room you will create a name
YOUR_MESSAGE = None  #put the message that you will post to the room


#sets the header to be used for authentication and data format to be sent.
def setHeaders():         
	accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}
	return (spark_header)

	
# creates a new room and returns the room id.
# Mission:  Add code to parse and return the room id
def createRoom(the_header,room_name):
	roomInfo = {"title":room_name}
	uri = 'https://api.ciscospark.com/v1/rooms'
	resp = requests.post(uri, data=roomInfo, headers=the_header)
	var = resp.json()
	print("createRoom JSON: ", var)	
	#MISSION: ADD CODE HERE TO PARSE AND RETURN THE ROOM ID.	
	return ("put your code here to parse room id from the var variable.")
	
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
	uri = None
	if uri == None:
		sys.exit("Please add the uri call to get room details.  See the Spark API Ref Guide")
	resp = requests.get(uri, headers=the_header)
	print("Room Info: ",resp.text)
	resp = resp.json
	print("put your code here to parse the resp variable and show room details")


if __name__ == '__main__':
	if ACCESS_TOKEN==None or ROOM_NAME==None or YOUR_MESSAGE==None:
		sys.exit("Please check that variables ACCESS_TOKEN, ROOM_NAME and YOUR_MESSAGE have values assigned.")
	header=setHeaders()
	#passing the ROOM_NAME for the room to be created
	room_id=createRoom(header,ROOM_NAME) 
	#passing roomId to members function here to add member to the room.
	addMembers(header,room_id)   
	#passing roomId to message function here to Post Message to a room.
	postMsg(header,room_id,YOUR_MESSAGE)
	#MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)
    
    
