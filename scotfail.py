import json
import requests

URL = "https://scotraiL.pw/live/"


def read_code_file():
    with open("codes.json") as f_d:
        return json.load(f_d)

def get_response(station_code):
    target = URL + station_code
    resp = requests.get(target)

    if resp.status_code != 200:
        raise Exception(resp.text)
    
    return json.loads(resp.text)


def get_services(station_code, destination):
    live = get_response(station_code)
    services = live["services"]

    if not destination:
        return [s for s in services]
    return [s for s in services if s["destination"] == destination]


def get_info(station_code, destination=None):
    services = get_services(station_code, destination)
    service_info = {}
    for service in services:
        info = {
            "platform": service["platform"],
            "arrives": service["arrives"],
            "expected": service["expected"],
            "destination": service["destination"],
            "origin": service["origin"]
        }
        service_info[service["departs"]] = info

    return service_info


def enquire(sc, dest=None):
    if not dest:
        info = get_info(sc)
    else:
        codes = read_code_file()
        info = get_info(sc, destination=codes[dest])

    if not info:
        print("No services.")
    else:
        print(info)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        enquire(sys.argv[1])
    else:
        enquire(sys.argv[1], dest=sys.argv[2])
