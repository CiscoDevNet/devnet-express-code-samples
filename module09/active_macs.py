import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64

def main():
        try:
            username = 'learning'
            password = 'learning'
            restURL = 'https://cmxlocationsandbox.cisco.com/api/location/v2/clients?sortBy=macAddress:ASC'
            request = requests.get(
            url = restURL,
            auth = HTTPBasicAuth(username,password),
            verify=False)

            macValues=[]
            jdata = json.loads(request.text)
            for d in jdata:
                for key, value in d.items():
                    if key == "macAddress":
                        macValues.append(value)

            print (macValues)

        except requests.exceptions.RequestException as e:
            print(e)
if __name__ == "__main__":
    main()
