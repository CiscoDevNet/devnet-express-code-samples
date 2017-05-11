#!/usr/bin/env python

# Import necessary modules
import requests

# Define necessary global variables
VIRL_URL = ""

USERNAME = "guest"
PASSWORD = "guest"


def create_project_user(url, username, password):
    '''
    This function will create a new project and a new user
    which will be associated with the project.
    '''
    print("Creating the project...")
    # Project URL against which the API call will be placed
    project_api = ""
    project_url = url + ":19400" + project_api

    # Below variables will be used to create new project
    project_name = ""
    description = "Project created via Python"
    enabled = True
    new_password = project_name

    # Parameters which will be passed to the server with the API call
    params = {"name": project_name,
              "description": description,
              "enabled": enabled,
              "user-password": new_password
              }

    # Make an API call and assign the response information to the variable
    project_response = requests.post(
        project_url, auth=(username, password), params=params)

    # Check if call was successful, if true print it
    if project_response.status_code == 200:
        print("\nProject was created successfully.\n\n")

    # Update global variables
    global USERNAME, PASSWORD
    USERNAME = new_password
    PASSWORD = new_password


def start_sim(url, username, password):
    '''
    This function will start a simulation using provided .virl file
    '''
    print("\nStarting simulation...\n")

    # Simulation start URL against which the API call will be placed
    simulation_start_api = ""
    simulation_start_url = url + ":19399" + simulation_start_api

    # Open .virl file and assign it to the variable
    virl_file = open('mission.virl', 'rb')

    # Parameter which will be passed to the server with the API call
    simulation_name = ''
    params = {'file': simulation_name}

    # Make an API call and assign the response information to the variable
    simulation_start_response = requests.post(
        simulation_start_url, auth=(username, password), params=params, data=virl_file)

    # Check if call was successful, if true print it and return the value
    if simulation_start_response.status_code == 200:
        print(simulation_start_response.text +
              " simulation has successfully started.\n\n")
        return simulation_start_response.text


def packet_capture(url, username, password, sim):
    '''
    This function will gather necessary information to start packet capturing process.
    Also, user is required to answer questions in order for function to do its job.
    '''
    # Node URL against which the API call will be placed
    node_api = ""
    node_url = url + ":19399" + node_api + "/" + sim

    # Make an API call and assign the response information to the variable
    node_response = requests.get(node_url, auth=(username, password)).json()

    # Create an empty dictionary, which will hold node information
    nodes = {}

    # Print columns identifiers
    print("\nNumber     Node")

    # Iterate over node_response and assign node information to nodes{}
    # dictionary
    for i, node in enumerate(node_response[sim]):

        # Check to see if node is not ~mgmt-lxc and then assign it
        if node != '~mgmt-lxc':
            nodes[i + 1] = node
            print(str(i + 1) + ":" + " " * 10 + node)

    # Variable which will hold a node name chosen by the user
    mission_node = ''

    # While loop helps to make sure that user chooses correct node
    while not mission_node:
        user_input = input("\nWhich node would you like to select? ")
        if user_input in nodes.values():
            mission_node = user_input
        else:
            print("\nYour choice is not valid. Please choose a valid node name.\n")
            print("\n\n\nNumber     Node")
            for num in nodes.keys():
                print(str(num)+ ":" + " " * 10 + nodes[num])

    # Interface URL against which the API call will be placed
    iface_api = ""
    iface_url = url + ":19399" + iface_api + "/" + sim

    # Parameters which will be passed to the server with the API call
    iface_params = {"simulation": sim,
                    "nodes": [mission_node]
                    }

    # Make an API call and assign the response information to the variable
    iface_response = requests.get(
        iface_url, auth=(username, password), params=iface_params).json()

    # Create an empty dictionary, which will hold interface information
    ifaces = {}

    # Print columns identifiers
    print("\n\n\nInterface ID      Interface Name")

    # Iterate over iface_response and assign interface information to ifaces{}
    # dictionary
    for i, iface in enumerate(iface_response[sim][mission_node]):
        # Check to see if interface is not management and then assign it
        if iface != 'management':
            ifaces[str(i)] = iface_response[sim][mission_node][iface]["name"]
            print(
                iface + " " * 17 + iface_response[sim][mission_node][iface]["name"])

    # Variable which will hold an interface ID chosen by the user
    mission_iface = ""

    while not mission_iface:
        user_input = input("\nOn which interface ID would "
                           "you like to start capturing packets? ")
        if user_input in ifaces.keys():
            mission_iface = user_input
        else:
            print("\nYour choice is not valid. Please select "
                  "a valid interface ID\n\n")
            print("Interface ID      Interface Name")
            for num in ifaces.keys():
                print(str(num) + " " * 17 + ifaces[num])

    # Capture URL against which the API call will be placed
    capture_api = ""
    capture_url = url + ":19399" + capture_api + "/" + sim

    # Parameters which will be passed to the server with the API call
    capture_params = {"simulation": sim,
                      "node": mission_node,
                      "interface": mission_iface
                      }

    # Make an API call and assign the response information to the variable
    capture_response = requests.post(
        capture_url, auth=(username, password), params=capture_params)

    # Check if call was successful, if true print it
    if capture_response.status_code == 200:
        print(capture_response.text)
        print("\n\nPacket capture was successfully started. "
              "\nGo to VIRL UWM page in order to download the .pcap file")


def stop_simulation(url, username, password, sim):
    '''
    This function will stop specified simulation
    '''

    # Stop URL against which the API call will be placed
    stop_api = ""
    stop_url = url + ":19399" + stop_api + "/" + sim

    # Make an API call and assign the response information to the variable
    stop_response = requests.get(stop_url, auth=(username, password))

    # Check if call was successful, if true print it and exit the application
    if stop_response.status_code == 200:
        input("\nSimulation has been stopped. "
              "Press any key to exit the application")
        exit()


def main():
    '''
    This function will start functions created above in desired order
    '''

    # start create_project_user(url, username, password) function
    create_project_user(VIRL_URL, USERNAME, PASSWORD)

    # start start_sim(url, username, password) function and assign the result
    # to the variable
    simulation = start_sim(VIRL_URL, USERNAME, PASSWORD)

    # Print a message asking user to verify that all nodes have an [ACTIVE -
    # REACHABLE] state

    print("Please go to VIRL UWM page and make sure all nodes \n"
          "are in active and reachable state. \n"
          "It should only take 2-3 minutes.")
    print("\nIf you proceed without waiting, the next function \n"
          "will create a non-functional .pcap file and you will \n"
          "not be able to download it from VIRL UWM page.\n")

    # While loop will run infinitely until user confirms that all nodes are
    # active and reachable
    while True:
        user_input = input(
            "\n\n\nAre all nodes in active and reachable state?(y/n)[n] ")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            break
        else:
            print(
                "\nOkay! Please wait until the nodes state changes to desired value")

    # start packet_capture(url, username, password, sim) function
    packet_capture(VIRL_URL, USERNAME, PASSWORD, simulation)

    # While loop will run infinitely until user confirms that he/she
    # downloaded the .pcap file
    while True:
        user_input = input(
            "\n\n\nWere you able to download .pcap file from VIRL UWM page?(y/n)[n] ")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            break
        else:
            print(
                "\nOkay! Go to VIRL UWM page and download the file. \n\
                When you are ready, come back to terminal screen and answer the question again")

    # Notify user that simulation will be stopped next
    print(
        "\nScript will now stop the node. You should see appropriate message briefly.\n")

    # start stop_simulation(url, username, password, sim) function
    stop_simulation(VIRL_URL, USERNAME, PASSWORD, simulation)


# Check if this python script has been run as a standalone program, if
# true run main() function
if __name__ == '__main__':
    main()
