#!/usr/bin/env python

from __future__ import print_function
import requests

HOST = '198.18.134.1'
USER = PASS = 'guest'


def simengineURL(cfg, verb, sim_id=None):
    """
    returns the URL for simengine based on the verb
    (list, status, launch, stop, ...)
    factor in sim_id as a path parameter, if present
    """
    sim = '' if sim_id is None else '/{}'.format(sim_id)
    fmt = dict(h=cfg['host'], v=verb, s=sim)
    # could use format_map() in Python 3.5
    return "http://{h}:19399/simengine/rest/{v}{s}".format(**fmt)


def auth(cfg):
    """
    returns a tuple for authentication
    using the username and the password
    from the cfg
    """
    return (cfg['username'], cfg['password'])


def listSims(cfg):
    """
    returns iterator for all sims on system
    """
    with cfg['session'] as s:
        r = s.get(simengineURL(cfg, 'list'), auth=auth(cfg))
    if r.ok:
        simulations = r.json().get('simulations')
        if simulations is not None:
            for sim_id in simulations.keys():
                yield sim_id


def startSim(cfg, fh):
    """
    start a sim, given the fh with a .virl file
    """
    params = dict(file=fh.name)
    fh.seek(0)
    with cfg['session'] as s:
        r = s.post(simengineURL(cfg, 'launch'),
                   params=params, data=fh, auth=auth(cfg))
    return r.text if r.ok else "none"


def startSims(cfg, filename, amount):
    with open(filename, "rb") as fh:
        for i in range(amount):
            print('Sim "{}" started'.format(startSim(cfg, fh)))


def stopSim(cfg, sim_id):
    """
    stop the given sim ID
    """
    with cfg['session'] as s:
        r = s.get(simengineURL(cfg, 'stop', sim_id), auth=auth(cfg))
    return r.ok


def stopSims(cfg):
    for sim in listSims(cfg):
        result = "stopped" if stopSim(cfg, sim) else "stop failed"
        print('Sim "{}" {}'.format(sim, result))


def main():
    virl = dict(session=requests.session(), host=HOST,
                username=USER, password=PASS)
    # startSims(virl, "two-containers.virl", 5)
    stopSims(virl)


if __name__ == '__main__':
    main()
