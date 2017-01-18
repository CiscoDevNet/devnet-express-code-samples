#!/usr/bin/env python
#
# Configure CMX notification
#
# darien@sdnessentials.com
#


import requests
from requests.auth import HTTPBasicAuth
import sys
requests.packages.urllib3.disable_warnings()

USERNAME = 'learning'
PASSWORD = 'learning'
URI = 'https://msesandbox.cisco.com:8081/api/config/v1/notification'
PAYLOAD = 'notification.json'


def main():
    """Simple main method to create a CMX notification."""
    try:
        f = open(PAYLOAD, 'r')
        data = f.read().replace('\n', '')
        # print(json.dumps(data))
        headers = {
            'content-type': "application/json",
            'accept': "application/json"
        }
        request = requests.put(url=URI,
                               auth=HTTPBasicAuth(USERNAME, PASSWORD),
                               data=data,
                               headers=headers,
                               verify=False)
        # print(request.status_code)
        print("Awesome! We were able to create our notification!")
    except requests.exceptions.RequestException as e:
        print("Oh no! We ran into the following error:")
        print(e)

if __name__ == '__main__':
    sys.exit(main())
