#!/usr/bin/env python
"""Mission for Module 08 to post Tropo number to Sparkc."""

import requests
import sys

sys.path.append('../../module03/03-environment-03-mission/')
import hello_lab
import myspark

# Disable warnings
requests.packages.urllib3.disable_warnings()
# Tropo API server
tropo_api = "https://api.tropo.com"
# Tropo network programmability application ID
tropo_app_id = "5068669"
# Tropo credentials
tropo_user = "dhirotsu"
tropo_pass = "0p0rT@v3ng3rs"
your_name = "Darien"


def phone_number(tropo_api, tropo_app_id, tropo_user, tropo_pass):
    """Function to retrieve Tropo application's phone number."""
    # Create the URI string for our Tropo application
    url = "{api}{address}{app}{addr}".format(api=tropo_api,
                                             address="/v1/applications/",
                                             app=tropo_app_id,
                                             addr="/addresses/")

    # Content type must be included in the header
    header = {"content-type": "application/json"}
    try:
        # Perform a GET on the Addresses endpoint to retrieve application data
        response = requests.get(url,
                                auth=(tropo_user, tropo_pass),
                                headers=header,
                                verify=False)
        # Convert response to JSON format
        r_json = response.json()
        # The result is a list with multiple entries
        for data in r_json:
            # Retrieve the value for "displayNumber" when "type" is "number"
            if data["type"] == "number":
                phone_number = data["displayNumber"]
                # Use the print statement below to test when needed
                # print(phone_number)
                return phone_number

    except Exception as e:
        print("Oops! We couldn't get the phone number of your application!")
        print("{error}".format(error=e))
        sys.exit()


def main():
    """Simply main function to post to Spark room."""
    try:
        app_number = phone_number(tropo_api, tropo_app_id, tropo_user, tropo_pass)
        room = myspark.spark_get_room_id(hello_lab.SPARK_TOKN, hello_lab.SPARK_ROOM)
        myspark.spark_send_message(hello_lab.SPARK_TOKN,
                                   room,
                                   "Hi! This is: {name}.".format(name=your_name))
        myspark.spark_send_message(hello_lab.SPARK_TOKN,
                                   room,
                                   "I just finished my first Tropo application!")
        myspark.spark_send_message(hello_lab.SPARK_TOKN,
                                   room,
                                   "Dial this number to try it out: {num}.".format(num=app_number))
        print("Awesome! Check the Spark chat room for you message.".format(room={room}))

    except Exception as e:
        print("On no! We couldn't post to the Spark room!")
        print("{error}".format(error=e))
        sys.exit()


if __name__ == '__main__':
    sys.exit(main())
