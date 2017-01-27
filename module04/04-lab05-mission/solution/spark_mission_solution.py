import json
import requests

#MISSION FILL IN THE REQUESTED DETAILS
ACCESS_TOKEN = "THIS_FIELD_HAS_TO_BE_POPULATED_BY_THE_STUDENT" #put your access token between the quotes
ROOM_NAME = "Module04 Mission Room" #give the room you will create a name. use ascii characters to avoid any unexpected results.
YOUR_MESSAGE = "My python script is working!"  #put the message that you will post to the room

#sets the header to be used for authentication and data format to be sent.
def setHeaders():         
    accessToken_hdr = 'Bearer ' + ACCESS_TOKEN
    spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json; charset=utf-8'}     
    return spark_header


# creates a new room and returns the room id.
# Mission:  Add code to parse and return the room id
def createRoom(the_header,room_name):
    roomInfo = '{"title" :"' + room_name + '"}'
    uri = 'https://api.ciscospark.com/v1/rooms'
    resp = requests.post(uri, data=roomInfo, headers=the_header)
    var = resp.json()
    #print("createRoom JSON: ", var)
    #MISSION: ADD CODE HERE TO PARSE AND RETURN THE ROOM ID.
    print("Room " + ROOM_NAME + " was successfully created.\n"
          "ID Number: " + var["id"])
    return var["id"]


# adds a new member to the room.  Member e-mail is test@test.com
def addMembers(the_header,roomId):
    member = '{"roomId":"' + roomId + '","personEmail": "test@test.com", "isModerator": false}'
    uri = 'https://api.ciscospark.com/v1/memberships'
    resp = requests.post(uri, data=member, headers=the_header)
    print("addMembers JSON: ", resp.json())

#posts a message to the room
def postMsg(the_header,roomId,message):
    message = '{"roomId":"' + roomId + '","text":"'+message+'"}'
    uri = 'https://api.ciscospark.com/v1/messages'
    resp = requests.post(uri, data=message, headers=the_header)
    print("postMsg JSON: ", resp.json())


def getRoomInfo(the_header,roomId):
#MISSION: WRITE CODE TO RETRIEVE AND DISPLAY DETAILS ABOUT THE ROOM YOU'VE CREATED
    uri = 'https://api.ciscospark.com/v1/rooms/' + roomId
    resp = requests.get(uri, headers=the_header)
    print("getRoomInfo JSON: ", resp.json())

if __name__ == '__main__':
    header=setHeaders()
    #passing the ROOM_NAME for the room to be created
    room_id=createRoom(header,ROOM_NAME)
    #passing roomId to members function here to add member to the room.
    addMembers(header,room_id)
    #passing roomId to message function here to Post Message to a room.
    postMsg(header,room_id,YOUR_MESSAGE)
  #MISSION: ADD FUNCTION CALL getRoomInfo(header,room_id)
    getRoomInfo(header,room_id)