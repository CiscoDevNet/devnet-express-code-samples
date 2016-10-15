#!/usr/bin/env python

from time import sleep
import requests
import logging

# Define some global variables
VIRL_URL = "http://198.18.134.1"
USERNAME = "guest"
PASSWORD = "guest"
MAX_WAIT = 300


# holds configuration information needed by all the functions
class VIRLConfig(object):

    '''
    docstring for VIRLConfig
    '''

    def __init__(self, logger, user, password, url,
                 timeout=MAX_WAIT, packets=1000, pcapfilter='',
                 sim_id=None, sim_node=None, sim_intfc=None):
        super(VIRLConfig, self).__init__()
        self.user = user
        self.password = password
        self.url = url
        self.timeout = timeout
        self.sim_id = sim_id
        self.sim_node = sim_node
        self.sim_intfc = sim_intfc
        self.logger = logger
        self.packets = packets
        self.filter = pcapfilter


def start_sim(cfg, filename):
    '''
    This function will start a simulation using provided .virl file
    '''
    # Simulation start URL against which the API call will be placed
    simulation_start_api = "/simengine/rest/launch"
    simulation_start_url = cfg.url + ":19399" + simulation_start_api

    cfg.logger.info('Simulation start...')

    # Open .virl file and assign it to the variable
    with open(filename, 'rb') as virl_file:
        # Parameter which will be passed to the server with the API call
        simulation_name = 'Mission'
        params = {'file': simulation_name}

        # Make an API call and assign the response information to the variable
        r = requests.post(simulation_start_url, auth=(cfg.user, cfg.password),
                          params=params, data=virl_file)

        # Check if call was successful, if true print it and return the value
        if r.status_code == 200:
            cfg.sim_id = r.text
            cfg.logger.info(
                'Simulation has been started, sim id [%s]', cfg.sim_id)
        else:
            cfg.logger.error('VIRL API "Simulation could not be started!"')
            cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))

    return r.ok


def wait_for_sim_to_start(cfg):
    '''
    returns True if the sim is started and all nodes
    are active/reachable
    waits for cfg.max_wait (default 5min)
    '''

    node_api = "/simengine/rest/nodes"
    node_url = cfg.url + ":19399" + node_api + "/" + cfg.sim_id

    interval = 10
    waited = 0
    active = False

    cfg.logger.info('Waiting for Simulation to become active...')

    while not active and waited < cfg.timeout:

        # Make an API call and assign the response information to the
        # variable
        r = requests.get(node_url, auth=(cfg.user, cfg.password))
        if not r.ok:
            cfg.logger.error('VIRL API "could not read sim state!"')
            cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))
            return False

        # check if all nodes are active AND reachable
        nodes = r.json()[cfg.sim_id]
        for node in nodes.values():
            if not (node.get('state') == 'ACTIVE' and node.get('reachable')):
                active = False
                break
            else:
                active = True

        # wait if not
        if not active:
            sleep(interval)
            waited = waited + interval

    if active:
        cfg.logger.info("Simulation is active.")
    else:
        cfg.logger.error("Timeout... aborting!")

    return active


def get_interface_id(cfg):
    '''
    get the interface index we're looking for
    '''
    cfg.logger.info("Getting interface id from name [%s]...", cfg.sim_intfc)

    iface_api = "/simengine/rest/interfaces"
    iface_url = cfg.url + ":19399" + iface_api + "/" + cfg.sim_id

    # Parameters which will be passed to the server with the API call
    iface_params = {"simulation": cfg.sim_id,
                    "nodes": cfg.sim_node
                    }

    # Make an API call and assign the response information to the variable
    r = requests.get(iface_url, auth=(cfg.user, cfg.password),
                     params=iface_params)
    if r.ok:
        interfaces = r.json().get(cfg.sim_id).get(cfg.sim_node)
        for key, interface in interfaces.items():
            if interface.get('name') == cfg.sim_intfc:
                cfg.logger.info("Found id: %s", key)
                return key
    else:
        cfg.logger.error('VIRL API "could not read interfaces!"')
        cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))

    cfg.logger.error("Can not find specified interface %s in simulation!",
                     cfg.sim_intfc)
    return None


def create_packet_capture(cfg):
    '''
    create a packet capture for the simulation using the given
    parameters in cfg
    '''
    cfg.logger.info("Starting packet capture...")

    # get interface based on name
    interface = get_interface_id(cfg)
    if interface is not None:
        capture_api = "/simengine/rest/capture"
        capture_url = cfg.url + ":19399" + capture_api + "/" + cfg.sim_id

        # Parameters which will be passed to the server with the API call
        capture_params = {"simulation": cfg.sim_id,
                          "node": cfg.sim_node,
                          "interface": interface,
                          "count": cfg.packets,
                          "pcap-filter": cfg.pcapfilter
                          }

        # Make an API call and assign the response information to the variable
        r = requests.post(capture_url, auth=(cfg.user, cfg.password),
                          params=capture_params)

        # did it work?
        if r.ok:
            retval = list(r.json().keys())[0]
            cfg.logger.info("Created packet capture (%s)", retval)
        else:
            cfg.logger.error('VIRL API "could not create capture!"')
            cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))
            retval = None

        return retval


def wait_for_packet_capture(cfg, id):
    '''
    wait until the packet capture is done. check for the 'running'
    state every 10 seconds.
    '''
    interval = 10
    waited = 0
    done = False

    capture_api = "/simengine/rest/capture"
    capture_url = cfg.url + ":19399" + capture_api + "/" + cfg.sim_id

    cfg.logger.info('Waiting for capture to finish...')

    while not done and waited < cfg.timeout:

        # Make an API call and assign the response information to the
        # variable
        r = requests.get(capture_url, auth=(cfg.user, cfg.password))
        if not r.ok:
            cfg.logger.error('VIRL API "could not read captures!"')
            cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))
            return False

        # check if all nodes are active AND reachable
        captures = r.json()
        for cid, cval in captures.items():
            if cid == id and not cval.get('running'):
                done = True
                break

        # wait if not
        if not done:
            sleep(interval)
            waited = waited + interval

    if done:
        cfg.logger.info("Capture has finished.")
    else:
        cfg.logger.error("Timeout... aborting!")

    return done


def download_packet_capture(cfg, id):
    '''
    download the finished capture and write it into a file
    '''

    content = 'application/vnd.tcpdump.pcap'
    capture_api = "/simengine/rest/capture"
    capture_url = cfg.url + ":19399" + capture_api + "/" + cfg.sim_id

    capture_params = {"capture": id}
    cfg.logger.info('Downloading capture file...')
    headers = dict(accept=content)

    # Make an API call and assign the response information to the
    # variable
    r = requests.get(capture_url, params=capture_params, headers=headers,
                     auth=(cfg.user, cfg.password))
    if not r.ok:
        cfg.logger.error('VIRL API "could not download capture!"')
        cfg.logger.error('%s: %s', r.status_code, r.json().get('cause'))
    elif r.status_code == 200 and r.headers.get('content-type') == content:
        # "ContentDisposition":
        # "attachment; filename=V1_GigabitEthernet0_1_2016-10-15-17-18-18.pcap
        filename = r.headers.get('Content-Disposition').split('=')[1]
        print(filename)
        with open(filename, "wb") as fh:
            fh.write(r.content)
    else:
        cfg.logger.error("problem... %s", r.headers)

    cfg.logger.info("Download finished.")


def stop_sim(cfg):
    '''
    This function will stop specified simulation
    '''
    cfg.logger.info('Simulation stop...')

    # Stop URL against which the API call will be placed
    stop_api = "/simengine/rest/stop"
    stop_url = cfg.url + ":19399" + stop_api + "/" + cfg.sim_id

    # Make an API call and assign the response information to the variable
    response = requests.get(stop_url, auth=(cfg.user, cfg.password))

    # Check if call was successful, if true print it and exit the application
    if response.status_code != 200:
        cfg.logger.error('VIRL API "could not stop simulation!"')
        cfg.logger.error(
            '%s: %s', response.status_code, response.json().get('cause'))
    else:
        cfg.logger.info('Simulation [%s] stop initiated.', cfg.sim_id)


def main():
    '''
    This function will start functions created above in desired order
    '''
    # setup the logging mechanics
    logger = logging.getLogger('VIRL')
    # change this to logging.ERROR for silence
    logger.setLevel(logging.DEBUG)
    FORMAT = '%(asctime)s %(funcName)s(): %(message)s'
    logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

    # use for the configuration & parameters for the capture
    config = VIRLConfig(logger, USERNAME, PASSWORD, VIRL_URL)
    config.sim_node = 'V1'
    config.sim_intfc = 'GigabitEthernet0/1'
    config.packets = 10
    config.pcapfilter = ''

    # start the simulation
    logger.info('Starting...')
    if start_sim(config, 'mission.virl'):
        # wait for all nodes to come up, maximum 300s = 5min)
        if wait_for_sim_to_start(config):
            cap_id = create_packet_capture(config)
            # wait for capture to finish
            if wait_for_packet_capture(config, cap_id):
                download_packet_capture(config, cap_id)
        # stop the sim (deletes also the captures)
        stop_sim(config)


# Check if this python script has been run as a standalone program, if
# true run main() function
if __name__ == '__main__':
    main()

