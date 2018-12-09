"""Small hacky script to check timetables for scotrail
Utilises the API supplied by https://github.com/rtgnx/scotrail-api
"""

import json
import requests

# API location
URL = "https://scotrail.pw/live/"


def read_code_file():
    """Reads the JSON file for station codes
    
    Returns:
        dict -- List of station codes and the station names
    """
    with open("codes.json") as f_d:
        return json.load(f_d)


def get_response(station_code):
    """Calls the API with the Station code to get the info
    
    Arguments:
        station_code {str} -- Three letter station code
    
    Raises:
        Exception -- Not a 200 response from the API
    
    Returns:
        dict -- Response as JSON
    """
    target = URL + station_code
    resp = requests.get(target)

    if resp.status_code != 200:
        raise Exception(resp.text)
    
    return json.loads(resp.text)


def get_services(station_code, destination):
    """Rips out the services from the response from the API
    
    Arguments:
        station_code {str} -- Three letter station code
        destination {str} -- Three letter code for destination station (Optional)
    
    Returns:
        list -- List of services from the Station
    """

    live = get_response(station_code)
    services = live["services"]

    if not destination:
        return [s for s in services]
    return [s for s in services if s["destination"] == destination]


def get_info(station_code, destination=None):
    """Builds info dict for services from a station
    Passing in a destination gives services going to that station
    
    Arguments:
        station_code {str} -- Three letter station code for target station
    
    Keyword Arguments:
        destination {str} -- Three letter station code for destination (Optional)
    
    Returns:
        dict -- Services from that station
    """

    services = get_services(station_code, destination)
    service_info = {}
    for service in services:
        if service["departs"] and service["arrives"]:
            info = {
                "platform": service["platform"],
                "arrives": service["arrives"],
                "expected": service["expected"],
                "destination": service["destination"],
                "origin": service["origin"]
            }

            service_info["Departure: " + service["departs"]] = info
        elif service["departs"]:
            info = {
                "platform": service["platform"],
                "expected": service["expected"],
                "destination": service["destination"],
                "origin": service["origin"]
            }
            service_info["Departure: " + service["departs"]] = info
        elif service["arrives"]:
            info = {
                "platform": service["platform"],
                "expected": service["expected"],
                "destination": service["destination"],
                "origin": service["origin"]
            }
            service_info["Arrival: " + service["arrives"]] = info

    return service_info


def enquire(sc, dest=None):
    """Query the API for train information
    
    Arguments:
        sc {str} -- Three letter station code for source station
    
    Keyword Arguments:
        dest {str} -- Three letter station code for destination (Optional)
    """

    codes = read_code_file()

    if not dest:
        info = get_info(sc)
    else:
        info = get_info(sc, destination=codes[dest])

    if not info:
        print("No services.")
    else:
        print(f"Services from {codes[sc]}\n")
        for service, s_info in info.items():
            if dest:
                print(f"From: {codes[sc]} To: {codes[dest]} ({service})")
            else:
                print(f"From: {codes[sc]} ({service})")
            for key, value in s_info.items():
                print(f"{key.capitalize()}: {value}")
            print()
            


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        enquire(sys.argv[1])
    else:
        enquire(sys.argv[1], dest=sys.argv[2])
