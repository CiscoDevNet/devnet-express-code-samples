#!/usr/bin/env python
#Mission for Module 08 to post your Tropo application phone number to Spark.

import requests
import sys
import json


# Disable warnings
requests.packages.urllib3.disable_warnings()


TROPO_API = "https://api.tropo.com/v1"  # Tropo API server
STATUS_OK = 200


#MISSION: fill in the variables below.
TROPO_APP_NAME	= "" # Your Tropo network application name.  Enter a different name if you named it something else.
TROPO_USER 		= ""   # Enter your Tropo user name
TROPO_PASS 		= ""   # Enter your Tropo password
YOUR_NAME  		= ""   # Enter your name
SPARK_TOKEN     = ""   # Enter your Spark token
SPARK_ROOM      = ""   # Enter the Spark room name that you are a member of to which you will post a message



# Function to retrieve Tropo application ID.
def get_tropo_app_id(tropo_api,app_name, tropo_user, tropo_pass):
	app_id=None
	# Content type must be included in the header
	header = {"content-type": "application/json"}
	api_call= "/applications"
	url= tropo_api + api_call
	response = requests.get(url,auth=(tropo_user,tropo_pass),headers=header,verify=False)
	if(response):		
		resp=response.json()
		for app in resp:
			if(app["name"]==app_name):
				app_id=app["id"]
				break
		if(app_id == None):
			print("The Tropo application with name " + app_name + " was not found!")
	else:
		print("No Tropo application returned for user.  Please check that the Tropo user and password are correct, and the user has applications.")
	return app_id

	
# Function to retrieve Tropo application's phone number.
def get_tropo_phone_number(tropo_api, tropo_app_id, tropo_user, tropo_pass):
	phone_num=None
	# Content type must be included in the header
	header = {"content-type": "application/json"}
	# Create the URI string for our Tropo application
	url = "{api}{address}{app}{addr}".format(api=tropo_api,
											address="/applications/",
											app=tropo_app_id,
											addr="/addresses")		
	response = requests.get(url,auth=(tropo_user,tropo_pass),headers=header,verify=False)
	if(response):				
		resp=response.json()
		for data in resp:
			# Retrieve the value for "displayNumber" when "type" is "number"
			if (data["type"] == "number"):
				phone_num = data["displayNumber"]
				break
			
	if(phone_num == None):
		print("The phone number for application id " + tropo_app_id + " was not found.")
		
	return phone_num

# Function to get the ID of the Spark room
def get_spark_room_id(token,room_name):
	room_id=None
	accessToken_hdr = 'Bearer ' + token
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json'}     	
	uri = 'https://api.ciscospark.com/v1/rooms'
	response = requests.get(uri,headers=spark_header)
	resp = response.json()
	for room in resp["items"]:		
		if(room["title"] == room_name):
			room_id=room["id"]
			break;
	if(room_id==None):
		print("Could not find Spark room " + room_name)
		
	return (room_id)

# Function to send a Spark message to a Spark Room
def send_spark_message(token,roomId,message):
	accessToken_hdr = 'Bearer ' + token
	spark_header = {'Authorization': accessToken_hdr, 'Content-Type': 'application/json'}     	
	message = '{"roomId":"' + roomId + '","text":"'+message+'"}'
	uri = 'https://api.ciscospark.com/v1/messages'
	resp = requests.post(uri, data=message, headers=spark_header)	
	if(resp.status_code!= STATUS_OK):
		print("Failed to send message to roomId: {room_id} ".format(room_id=roomId))
	

#Main engine function
def main():    
	app_id=get_tropo_app_id(TROPO_API,TROPO_APP_NAME,TROPO_USER,TROPO_PASS)
	if(app_id != None):
		phone_num = get_tropo_phone_number(TROPO_API,app_id,TROPO_USER,TROPO_PASS)
		if(phone_num != None):
			room_id = get_spark_room_id(SPARK_TOKEN,SPARK_ROOM)
			if(room_id != None):
				send_spark_message(SPARK_TOKEN,room_id,"Hi! This is {name}. I just finished my first Tropo application!".format(name=YOUR_NAME))
				send_spark_message(SPARK_TOKEN,room_id,"Dial this number to try it out: {num}.".format(num=phone_num))
			else:
				print("The Spark Room " + SPARK_ROOM + " was not found!")
			   
	if(app_id!=None and phone_num != None and room_id != None):
		print('Awesome! Check the Spark room "' + SPARK_ROOM + '" for your message.')


if __name__ == '__main__':
	sys.exit(main())
