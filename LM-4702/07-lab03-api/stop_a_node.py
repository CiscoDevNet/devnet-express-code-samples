# Importing module(s)
import requests
import json

# VIRL URL and API Call
VIRL_URL = "http://198.18.134.1:19399/"

# Username and password
USERNAME = "guest"
PASSWORD = "guest"

def running_sim(url, username, password):

    # Set the API call variable
    running_sim_api = "/simengine/rest/list"

    # Combine the url and the API call
    url += running_sim_api

    headers = {'content-type': 'text/xml'}

    # Make a request call with method get to the VIRL server
    response = requests.get(url, auth=(username, password), headers=headers).json()

    # Print how many active simulations were found.
    print("\n\nVIRL reports " + str(len(response["simulations"])) + " active simulations. They are: ")

    # Iterate over the response and print each simulation to the user.
    # If user recognizes the simulation return it.
    for sim in response["simulations"]:
        print("\n"+sim)
        user_input = input("Is this the simulation you are looking for?[Y/n] ")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            return sim



SIMULATION=running_sim(VIRL_URL,USERNAME,PASSWORD)


def nodes_in_sim(url, username, password, sim):

    # Set the API call variable
    running_sim_api = "/simengine/rest/nodes/" + sim

    # Combine the url and the API call
    url += running_sim_api

    headers = {'content-type': 'text/xml'}

    # Make a request call with method get to the VIRL server
    response = requests.get(url, auth=(username, password), headers=headers).json()

    # Print how many active nodes are in the simulations and choose a number of nodes to be stopped.
    num_nodes = int(input("\n\nVIRL reports " + str(len(response[sim])) +
	                         " active nodes in the simulation. \n" +
	                          "How many would you like to stop? [1-" + str(len(response[sim])) +
                              "] "))

    # Create an empty dictionary which will contain all nodes information
    all_nodes = {}

    # Iterate over the response and add each node to all_nodes list.
    for i, node in enumerate(response[sim]):
        all_nodes[i] = node
        print(str(i+1) +": " + node)
        print("    State: " + response[sim][node]["state"] +"\n")

    # Create an empty list which will hold user's chosen nodes
    # that will be shutdown by the code
    nodes = []

    # While num_nodes does not equal to zero run below code
    while num_nodes != 0:
        user_input = input("\n\n\nEnter the name of the node that you would like to shutdown. \n" +
       	                "Please choose a node in ACTIVE state: ")
        if user_input in all_nodes.values():
            nodes.append(user_input)
            num_nodes -= 1
            if num_nodes != 0:
                print("Roger that! You need to choose " + str(num_nodes) + " more node(s)")
        else:
            print("Your entry was incorrect please try again!\n\n\n")

    # Return chosen nodes
    return nodes

NODES = nodes_in_sim(VIRL_URL,USERNAME,PASSWORD, SIMULATION)

def stop_nodes(url, username, password, sim, nodes):

    # Set the API call variable
    running_sim_api = "/simengine/rest/update/" + sim + "/stop"

    # Combine the url and the API call
    url += running_sim_api

    headers = {'content-type': 'text/xml'}

    # Define an empty dictionary which will hold parameters information
    params = {}
    for node in nodes:
        params['nodes'] = node

        # Make a request call with method put to the VIRL server
        response = requests.put(url, auth=(username, password), params=params, headers=headers)

        # Check if the code execution was successful
        if response.status_code == 200:
            print("\nSuccessfully stopped " + node)




stop_nodes(VIRL_URL,USERNAME,PASSWORD, SIMULATION, NODES)
