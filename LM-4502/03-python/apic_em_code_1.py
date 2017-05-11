# Import necessary modules
import requests
import json

# Disable warnings
requests.packages.urllib3.disable_warnings()

# Variables
apic_em_ip = "https://198.18.129.100/api/v1"

def get_token(url):

    # Define API Call
    api_call = "/ticket"

    # Payload contains authentication information
    payload = {"username": "admin", "password": "C1sco12345"}

    # Header information
    headers = {
        "content-type": "application/json"
    }

    # Combine URL, API call and parameters variables
    url += api_call

    response = requests.post(url, data=json.dumps(payload), headers=headers, verify=False)
    response.raise_for_status()
    response = response.json()

    # Return authentication token from respond body
    return response["response"]["serviceTicket"]


def get_device_id(token, url):

    # Define API Call
    api_call = "/network-device"

    # Header information
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call and parameters variables
    url += api_call

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    response = response.json()

    # Iterate over the response and find first device with access role.
    # Return ID number of the first device matching the criteria
    for item in response['response']:
        if item['role'] == 'ACCESS' and not item['family'] == 'Unified AP':
            return item['id']


def get_config(token, url, id):

    # Define API Call. To get specific device's configuration
    # we will need to add device's ID in the API call
    api_call = "/network-device/" + id + "/config"

    # Header information
    headers = {"X-AUTH-TOKEN": token}

    # Combine URL, API call variables
    url += api_call

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    response = response.json()

    # Create a file in present working directory
    file = open('access_host_1.txt', 'w')

    # Write response body to the file
    file.write(response['response'])

    # Close the file when writing is complete
    file.close()


# Assign obtained authentication token to a variable. Provide APIC-EM's
# URL address
auth_token = get_token(apic_em_ip)

# Assign obtained ID to a variable. Provide authentication token and
# APIC-EM's URL address
device_id = get_device_id(auth_token, apic_em_ip)

# Call get_config() function to obtain and write device's configuration to a file.
# Provide authentication token, APIC-EM's URL address and device's ID
get_config(auth_token, apic_em_ip, device_id)
