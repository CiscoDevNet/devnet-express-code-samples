import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64
import time

def main():
        try:
            username = 'learning'
            password = 'learning'
            restURL = 'https://cmxlocationsandbox.cisco.com/api/location/v2/clients/count'
            request = requests.get(
            url = restURL,
            auth = HTTPBasicAuth(username,password),
            verify=False)

            str_request = request.json()
            clientcount = str_request['count']

            print (clientcount)

        except requests.exceptions.RequestException as e:
            print(e)
if __name__ == "__main__":
    main()
