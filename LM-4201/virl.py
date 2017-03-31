#!/usr/bin/env python

try:
    input = raw_input
except NameError:
    pass

# Import necessary modules
import requests

# Define necessary global variables
VIRL_URL = "http://198.18.134.1"

USERNAME = "guest"
PASSWORD = "guest"


def start_sim(sim_file):
    """This function starts a simulation using the provided .virl file."""
    print("\nStarting simulation...\n")

    # Simulation start URL against which the API call will be placed
    simulation_start_api = "/simengine/rest/launch"
    simulation_start_url = VIRL_URL + ":19399" + simulation_start_api

    # Open .virl file and assign it to the variable
    virl_file = open("./sims/" + sim_file, 'rb')

    # Parameter which will be passed to the server with the API call
    simulation_name = sim_file.split('.')[0]
    params = {'file': simulation_name}

    # Make an API call and assign the response information to the variable
    simulation_start_response = requests.post(
        simulation_start_url, auth=(USERNAME, PASSWORD), params=params, data=virl_file)

    # Check if call was successful, if true print it and return the value
    if simulation_start_response.status_code == 200:
        print(simulation_start_response.text +
              " simulation has successfully started.\n\n")
        return True, simulation_start_response.text
    else:
        error_code = simulation_start_response.status_code
        error_reason = simulation_start_response.json().get('cause', 'UNKNOWN')
        print("VIRL returned %s code and failed to start the simulation.\n Reason is %s" % (error_code, error_reason))
        return False, error_code, error_reason


def stop_sim(sim_id):
    """This function will stop specified simulation."""
    # Stop URL against which the API call will be placed
    stop_api = "/simengine/rest/stop"
    stop_url = VIRL_URL + ":19399" + stop_api + "/" + sim_id

    # Make an API call and assign the response information to the variable
    stop_response = requests.get(stop_url, auth=(USERNAME, PASSWORD))

    # Check if call was successful, if true print it and exit the application
    print("FROM STOP VIRL " + stop_response.text)
    print(stop_response.status_code)
    if stop_response.status_code == 200:
        return True
    else:
        return False


def main():
    """This function will start functions created above in desired order."""
    # start start_sim(sim_file) function and assign the result to the variable
    simulation = start_sim('virl_topo.virl')

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
        user_input = input("\n\n\nAre all nodes in active and reachable state?(y/n)[n] ")
        if user_input.lower().strip() == 'y' or user_input.lower().strip() == 'yes':
            break
        else:
            print(
                "\nOkay! Please wait until the nodes state changes to desired value")

    # Notify user that simulation will be stopped next
    print(
        "\nScript will now stop the node. You should see appropriate message briefly.\n")

    # start stop_simulation(sim) function
    stop_sim(simulation)


# Check if this python script has been run as a standalone program, if
# true run main() function
if __name__ == '__main__':
    main()
