import sys
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64
import collections

'''
Python script "mac_history" prompts for a mac address and retrieves the historical location data for it.
Copy the python script called mac_history.py from the /module09 folder.
Run the script using the command $python3 mac_history.py.
Modify the script to extract the timestamp, coordinates and map hierarchy for each record.
Put the results in a Set in chronological order, such that a historical path of the client is created.
'''

def main():
  print("********************************************************");
  print("* Cisco CMX MAC History Python 3 Utility                  *");
  print("* Please provide the input in the following format     *");
  print("*                                                      *");
  print("* macAddress: 00:00:2a:01:00:06                        *");
  print("*                                                      *");
  print("* Control C to exit                                    *");
  print("********************************************************");

  username = 'learning'
  password = 'learning'
  restURL1 = 'https://cmxlocationsandbox.cisco.com/api/location/v1/historylite/clients/'

  while True:

       x          = None
       y          = None
       chgOn      = None
       flr        = None
       macAddress = None

       macAddress = input("macAddress: ")

       try:
           response = requests.get(
           url = restURL1 +"/"+ macAddress,
           auth = HTTPBasicAuth(username,password),
           verify=False)

           json_data = response.json()

           x = json_data["Data"][0]["x"]
           y = json_data["Data"][0]["y"]
           chgOn = json_data["Data"][0]["chgOn"]
           flr = json_data["Data"][0]["flr"]
           d = collections.OrderedDict()
           d['x'] = x
           d['y'] = y
           d['chgOn'] = chgOn
           d['flr'] = flr

           for k, v in d.items():
               print (k, v)

       except requests.exceptions.RequestException as e:
           print(e)


       print("----------------------------------------------------------------")
       print("x, y coordinates: ", x , ", " , y)
       print("timestamp (lastLocatedTime): "+ chgOn)
       print("floor: ", flr)
       print("----------------------------------------------------------------")
       print("\nControl C to Exit");

if __name__ == '__main__':
    main()

'''
{
  "Data": [
    {
      "x": 209.99107,
      "y": 38.91461,
      "flr": "723413320329068590",
      "chgOn": "1492780699608",
      "s": "1",
      "ssid": "test",
      "ap": "00:2b:01:00:02:00",
      "un": "",
      "ip": "10.10.20.165",
      "lat": -999,
      "long": -999
    },
'''
