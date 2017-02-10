#!/usr/bin/env python
# Importing module(s)
import requests
import json
import platform
import os

# VIRL URL and API Call
VIRL_URL = "http://198.18.134.1:19399/"

# Username and password
USERNAME = "guest"
PASSWORD = "guest"


def running_sim():

    # Set the API call variable
    running_sim_api = "/simengine/rest/list"

    # Combine the url and the API call
    URL = VIRL_URL + running_sim_api

    headers = {'content-type': 'text/xml'}

    # Make a request call with method get to the VIRL server
    response = requests.get(
        URL, auth=(USERNAME, PASSWORD), headers=headers).json()

    # Print how many active simulations were found.
    print("\n\nVIRL reports " +
          str(len(response["simulations"])) + " active simulations. They are: ")

    # Iterate over the response and print each simulation to the user.
    # If user recognizes the simulation return it.
    for sim in response["simulations"]:
        print("\n" + sim)
        user_input = input("Is this the simulation you are looking for?[Y/n] ")
        if user_input.lower() == 'y' or user_input.lower() == 'yes':
            return sim


def nodes_in_sim(sim_id, state="ACTIVE"):

    # Set the API call variable
    running_sim_api = "/simengine/rest/nodes/" + sim_id

    # Combine the url and the API call
    URL = VIRL_URL + running_sim_api

    headers = {'content-type': 'text/xml'}

    # Make a request call with method get to the VIRL server
    response = requests.get(
        URL, auth=(USERNAME, PASSWORD), headers=headers).json()

    # Print how many active nodes are in the simulations and choose a number
    # of nodes to be stopped.
    num_nodes = 1

    # Create an empty dictionary which will contain all nodes information
    all_nodes = {}

    # Iterate over the response and add each node to all_nodes list.
    for i, node in enumerate(response[sim_id]):
        if response[sim_id][node]["state"] == state:
            all_nodes[i] = node
            print(str(i + 1) + ": " + node)
            print("    State: " + response[sim_id][node]["state"] + "\n")


    # Create an empty list which will hold user's chosen nodes
    # that will be shutdown by the code
    nodes = []
    # While num_nodes does not equal to zero run below code
    while num_nodes != 0:
        user_input = input("\n\n\nEnter the name of the node that you would like to shutdown. \n" \
                           "Please choose a node in %s state: " % state)
        if user_input in all_nodes.values():
            nodes.append(user_input)
            num_nodes -= 1
            if num_nodes != 0:
                print("Roger that! You need to choose " +
                      str(num_nodes) + " more node(s)")
        else:
            print("Your entry was incorrect please try again!\n\n\n")

    # Return chosen nodes
    return nodes


def stop_nodes(sim_id, nodes):

    # Set the API call variable
    running_sim_api = "/simengine/rest/update/" + sim_id + "/stop"

    # Combine the url and the API call
    URL = VIRL_URL + running_sim_api

    headers = {'content-type': 'text/xml'}

    # Define an empty dictionary which will hold parameters information
    params = {}
    for node in nodes:
        params['nodes'] = node

        # Make a request call with method put to the VIRL server
        response = requests.put(
            URL, auth=(USERNAME, PASSWORD), params=params, headers=headers)

        # Check if the code execution was successful
        if response.status_code == 200:
            print("\nSuccessful stopped " + node)

def start_nodes(sim_id, nodes,):
    # Set the API call variable
    running_sim_api = "/simengine/rest/update/" + sim_id + "/start"

    # Combine the url and the API call
    URL = VIRL_URL + running_sim_api

    headers = {'content-type': 'text/xml'}

    # Define an empty dictionary which will hold parameters information
    params = {}
    for node in nodes:
        params['nodes'] = node

        # Make a request call with method put to the VIRL server
        response = requests.put(
            URL, auth=(USERNAME, PASSWORD), params=params, headers=headers)

        # Check if the code execution was successful
        if response.status_code == 200:
            print("\nSuccessful started " + node)

def clear_scr():
    platform_name = platform.system()
    if platform_name == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def main():

    while True:
        clear_scr()
        print("1. Get running simulation ID, choose desired node and stop it\n"
              "2. Get running simulation ID, choose desired node and start it\n"
              "3. Exit\n")
        usr_in = input("Choose a number of desired action: ")
        if usr_in == "1":
            # Obtain a name of a simulation and assign it to the variable
            SIMULATION = running_sim()
            clear_scr()
            # Get the nodes which user wants to shutdown and assign it to the variable
            NODES = nodes_in_sim(SIMULATION)
            # Stop the nodes and finish the script
            stop_nodes(SIMULATION, NODES)
            input("Press any key to return to the main menu!")
        elif usr_in == "2":
            # Obtain a name of a simulation and assign it to the variable
            SIMULATION = running_sim()
            clear_scr()
            # Get the nodes which user wants to shutdown and assign it to the variable
            NODES = nodes_in_sim(SIMULATION, state="ABSENT")
            # Start the nodes and finish the script
            start_nodes(SIMULATION, NODES)
            input("Press any key to return to the main menu!")
        elif usr_in == "3":
            exit()
        else:
            input("Your input was incorrect. Press any key to start again!")

main()