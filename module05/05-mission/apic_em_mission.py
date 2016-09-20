# import requests library
import requests

# import json library
import json

# Disable warnings
requests.packages.urllib3.disable_warnings()

# controller = IP Address of the controller
controller = ""

# Authentication Token obtained from Spark's Developer page
auth = ""

def getTicket():
    # Provide APIC-EM's username
    username = ""

    # Provide password for the username defined above
    password = ""

    # put the ip address or dns of your apic-em controller in this url
    url = "https://" + controller + "/api/v1/ticket"

    # the username and password to access the APIC-EM Controller
    payload = {"username": username, "password": password}

    # Content type must be included in the header
    header = {"content-type": "application/json"}

    # Performs a POST on the specified url to get the service ticket
    response = requests.post(url, data=json.dumps(
        payload), headers=header, verify=False)

    print(response)

    # convert response to json format
    r_json = response.json()

    # parse the json to get the service ticket
    ticket = r_json["response"]["serviceTicket"]
    
    return ticket


def getTopology(ticket):

    # Final Result
    result = []

    # API Call to retrieve physical topology
    api_call = ""

    # URL for topology REST API call to get list of existing devices on the
    # network, and build topology
    url = "https://" + controller + "/api/v1" + api_call

    # Content type as well as the ticket must be included in the header
    header = {"content-type": "application/json", "X-Auth-Token": ticket}

    # this statement performs a GET on the specified network device url
    response = requests.get(url, headers=header, verify=False)

    # convert data to json format.
    r_json = response.json()

    # Iterate through network device data and list the nodes, their
    # interfaces, status and to what they connect
    for n in r_json["response"]["nodes"]:
        found = 0  # print header flag
        printed = 0  # formatting flag
        for i in r_json["response"]["links"]:
            # Find interfaces that link to this one which means this node is
            # the target.
            if i["target"] == n["id"]:
                if found == 0:
                    if printed == 1:
                        print()
                    #print('{:>10}'.format("Source") + '{:>30}'.format("Source Interface") + '{:>25}'.format("Target Interface") + '{:>13}'.format("Status"))
                    result.append('\n' + '{:>10}'.format("Source") + '{:>30}'.format(
                        "Source Interface") + '{:>25}'.format("Target Interface") + '{:>13}'.format("Status"))
                    found = 1
                for n1 in r_json["response"]["nodes"]:
                    # find name of node to that connects to this one
                    if i["source"] == n1["id"]:
                        if "startPortName" in i:
                            #print("    " + '{:<20}'.format(n1["label"]) + '{:<25}'.format(i["startPortName"]) + '{:<23}'.format(i["endPortName"]) + '{:<8}'.format(i["linkStatus"]))
                            result.append("    " + '{:<20}'.format(n1["label"]) + '{:<25}'.format(
                                i["startPortName"]) + '{:<23}'.format(i["endPortName"]) + '{:<8}'.format(i["linkStatus"]))
                        else:
                            #print("    " + '{:<20}'.format(n1["label"]) + '{:<25}'.format("unknown") + '{:<23}'.format("unknown") + '{:<8}'.format(i["linkStatus"]))
                            result.append("    " + '{:<20}'.format(n1["label"]) + '{:<25}'.format(
                                "unknown") + '{:<23}'.format("unknown") + '{:<8}'.format(i["linkStatus"]))
                        break
    return(result)


def get_roomID():
    # API Call for rooms
    api_call = "rooms"

    # Please provide your personal authorization token bellow


    # Cisco Spark's API URL address
    url = "https://api.ciscospark.com/v1/" + api_call

    # Content type as well as the authorization must be included in the header
    header = {"content-type": "application/json; charset=utf-8",
              "Authorization": "Bearer " + auth}

    # this statement performs a GET on the specified network device url
    response = requests.get(url, headers=header, verify=False)
    r_json = response.json()

    for item in r_json["items"]:
        print("Title " + item["title"])
        print("Room ID " + item["id"] + "\n\n")
        user_input = input(
            "Is this the room you are looking for to post?[y/n] ")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            return item["id"]
        else:
            continue


def post_spark(text, room_id):
    """
    This function will post your text to DevNet Express Room in Spark
    """
    # API Call to for messages
    api_call = "messages"

    # Cisco Spark's API URL address
    url = "https://api.ciscospark.com/v1/" + api_call

    # Content type as well as the authorization must be included in the header
    header = {"content-type": "application/json; charset=utf-8",
              "Authorization": "Bearer " + auth}

    payload = {
        "roomId": room_id,
        "text": '\n'.join(text)
    }
    # this statement performs a GET on the specified network device url
    response = requests.post(url, data=json.dumps(
        payload), headers=header, verify=False)

    print("\nCheck the Spark Room, you just posted a message!")


if __name__ == "__main__":
    # Get authentication ticket from APIC-EM
    theTicket = getTicket()

    # Use authentication ticket to get the topology information
    message = getTopology(theTicket)

    # Get the room ID
    id = get_roomID()

    # Use room ID and retrieved topology information to post in the Spark
    post_spark(message, id)
