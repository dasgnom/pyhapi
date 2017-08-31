#!/usr/bin/env python3
import json
from hapi import station, networks
from pathlib import Path
import os.path


def get_config_file():
    """
    returns absolute path of config file
    :return: (string) absolute path of config file
    """
    home = str(Path.home())
    config = os.path.join(home, '.hapi')
    return config


def set_accessid(accessId, network):
    """
    save your api key
    :param accessId: your hapi api key
    :return: True if api key was saved successfully, else False
    """
    config = get_config()
    if not config:
        config = {}

    if network not in config:
        config[network] = {}
    config[network]['accessId'] = accessId
    try:
        with open(get_config_file(), 'w+') as f:
            json.dump(config, f)
    except:
        return False
    return True


def set_config_item(items):
    config = get_config()
    if not config:
        config = {}

    for item in items.keys():
        config[item] = items[item]

    with open(get_config_file(), 'w+') as f:
        json.dump(config, f)
    return True


def get_config():
    """
    ties to get api key from config
    :return: (dict) config
    """
    if not os.path.exists(get_config_file()):
        return False
    with open(get_config_file()) as f:
        config = json.load(f)

    if not config:
        return False
    return config


def search_station_by_name():
    config = get_config()
    nwconf = config['network']
    if 'accessId' in config[nwconf]:
        accessId = config[config['network']]['accessId']
    else:
        accessId = False
    name = input('station name: ')

    stat = station.Station(config['network'], accessId)
    stationlist = stat.searchName(name.strip())
    noStation = True

    for s in stationlist['stopLocationOrCoordLocation']:
        if not 'StopLocation' in s:
            continue
        s = s['StopLocation']
        print('{} - {}'.format(s['extId'], s['name']))
        noStation = False

    if noStation:
        print('No station found :(')


def search_station_by_coordinate():
    config = get_config()

    lat = input('latitude: ')
    lon = input('longitude: ')

    stat = station.Station(config['network'], config[config['network']]['accessId'])
    stationlist = stat.searchCoordinate(lat, lon)

    noStation = True

    if not 'stopLocationOrCoordLocation' in stationlist:
        print('No station found :(')
    for s in stationlist['stopLocationOrCoordLocation']:
        if not 'StopLocation' in s:
            continue
        s = s['StopLocation']
        print('{} - {}'.format(s['extId'], s['name']))
        noStation = False

    if noStation:
        print('No station found :(')

def clear_accessid(network):
    config = get_config()
    if 'accessId' not in config[network]:
        return True
    del(config[network]['accessId'])
    with open(get_config_file(), 'w+') as f:
        json.dump(config, f)
    return True


def select_network():
    nw = networks.networks
    nwlist = []
    for netw in nw.keys():
        print('{}) {}'.format(netw, nw[netw]['longname']))
        nwlist.append((netw))

    choice = input('select a network: ').strip()
    if choice not in nwlist:
        print('Invalid choice')
        exit(30)

    set_config_item({'network': choice})
    return True




if __name__ == '__main__':
    while True:
        config = get_config()
        if not config:
            select_network()
            config = get_config()

        if 'network' in config:
            print('You are working on network: {}'.format(config['network']))
        network = config['network']
        if network not in config:
            config[network] = {}
        if networks.networks[network]['accessId'] == True and 'accessId' not in config[network]:
            accessId = input('Please enter your AccessId: ')
            if not set_accessid(accessId, network):
                print('unable to write config file')
                exit(20)

        if 'network' not in config:
            select_network()

        print('Choose an option:')
        print('a) Search station by name')
        print('b) Search stations around coordinate')
        print('c) Show departures')
        print('--- settings ---')
        print('1) select network')
        print('0) clear accessId')
        print('----- quit -----')
        print('q) quit')
        print()
        choice = input('Your choice: ')

        if choice not in ['a', 'b', 'c', 'q', '0', '1']:
            print('Invalid choice')
            exit(1)

        if choice == 'a':
            search_station_by_name()
        elif choice == 'b':
            search_station_by_coordinate()
        elif choice == '0':
            clear_accessid(config['network'])
        elif choice == '1':
            select_network()
        elif choice == 'q':
            exit(0)
