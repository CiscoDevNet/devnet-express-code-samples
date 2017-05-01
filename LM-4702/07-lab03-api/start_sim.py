# Importing module(s)
import requests

# VIRL URL and API Call
virl_url = "http://198.18.134.1:19399/"
api_call = "/simengine/rest/launch"

virl_url += api_call 

# Username and password
username = "guest"
password = "guest"

# Open the API.virl file
virl_file=open('API.virl', 'rb')

# Create headers and payload information
headers = {'content-type': 'text/xml'}
payload = {'file': 'API_Launched'}

# Response variable will hold information obtained during the API call

response = requests.post(virl_url, auth=(username, password), params=payload, data=virl_file, headers=headers)

# Check to see if the response code is 200.
# If true, print "Simulation started successfully"
if response.status_code == 200:
    print("Simulation started successfully")
    print("Your simulation's name is " + response.text)
else:
	print("Simulation not started. Status ",response.status_code)
