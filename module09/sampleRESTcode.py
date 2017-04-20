import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64

def main():
   print("*********************************************************************************");
   print("* Cisco CMX Command Line REST API Python 3 Utility                              *");
   print("* Please provide the input in the following format                              *");
   print("*                                                                               *");
   print("* REST URL: https://cmxlocationsandbox.cisco.com/api/location/v2/clients/count  *");
   print("* Username: learning                                                            *");
   print("* Password: learning                                                            *");
   print("*                                                                               *");
   print("*                                                                               *");
   print("* Control C to exit                                                             *");
   print("*********************************************************************************");

   storedCredentials = False
   username = None
   password = None

   while True:
       restURL = input("\nREST URL: ")

       if not storedCredentials:
           username = input("Username: ")
           password = input("Password: ")
           storedCredentials = True

           print("----------------------------------")
           print(repr(restURL))
           print("Authentication string: "+ username+":"+password)
           print("----------------------------------")

       try:
           request = requests.get(
           url = restURL,
           auth = HTTPBasicAuth(username,password),
           verify=False)

           parsed = request.json
           print(json.dumps(parsed(), indent=2))

       except requests.exceptions.RequestException as e:
           print(e)

       print("\nControl C to Exit");

if __name__ == "__main__":
   main()
