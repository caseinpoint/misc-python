from json import dump, load, loads
from os.path import exists
from pprint import pprint
import random
from re import compile, IGNORECASE
from requests import get
from secrets import choice
from subprocess import run

REGEX_SIGNAL = compile(r'Signal level=(?P<signal>-\d+)', IGNORECASE)

API_URL = 'https://api.weather.gov'
API_HEADERS = {'User-Agent': '(randomseedapp.py, drues.other.email@gmail.com)'}


def cal_stations():
    """Create JSON file with all California weather stations."""

    ca_zones_query_res = get(url=API_URL+'/zones/public',
                                headers=API_HEADERS,
                                params={'area': 'CA'})
    ca_zones_data = ca_zones_query_res.json()
    stations = []
    for feature in ca_zones_data['features']:
        for station in feature['properties']['observationStations']:
            stations.append(station)
    with open('./calStations.json', 'w') as f:
        dump(stations, f)


if not exists('./calStations.json'):
    cal_stations()
with open('./calStations.json') as f:
    CAL_STATIONS = load(f)


def get_weather_seed(num_bytes=64):
    station_url = choice(CAL_STATIONS)
    station_query_res = get(url=station_url+'/observations',
                            headers=API_HEADERS,
                            params={'limit': 4})
    station_data = station_query_res.json()

    while len(station_data['features']) == 0:
        station_url = choice(CAL_STATIONS)
        station_query_res = get(url=station_url+'/observations',
                                headers=API_HEADERS,
                                params={'limit': 1})
        station_data = station_query_res.json()

    values = []
    for feature in station_data['features']:
        for key, property in feature['properties'].items():
            if isinstance(property, dict):
                if property['value'] is not None and property['value'] != 0:
                    values.append(key + str(property['value']))

    value_choice = choice(values)
    random.seed(value_choice)
    return random.randbytes(num_bytes)


def get_wifi_seed(num_bytes=64):
    wifi_scan_result = run(['sudo', 'iwlist', 'scan'],
                           capture_output=True,
                           encoding='locale')

    signals = REGEX_SIGNAL.findall(wifi_scan_result.stdout)
    signal_choice = choice(signals)
    random.seed(signal_choice)
    return random.randbytes(num_bytes)


def extract_inputs(input_dict, results=[]):
    """Recursively extract all non-zero values where key ends with '_input'."""

    for key, val in input_dict.items():
        if isinstance(val, dict):
            extract_inputs(val, results)
        elif key.endswith('_input') and val != 0:
            results.append(key + str(val))
    return results


def get_cpu_seed(num_bytes=64):
    cpu_result = run(['sensors', '-j'],
                     capture_output=True,
                     encoding='locale')
    json_result = loads(cpu_result.stdout)
    # pprint(json_result)
    inputs = extract_inputs(json_result)
    sensor_choice = str(choice(inputs))
    random.seed(sensor_choice)
    return random.randbytes(num_bytes)


if __name__ == '__main__':
    print('test output:')

    # for _ in range(10):
    cpu_seed = get_cpu_seed(num_bytes=64//3)
    print(f'cpu_seed: {cpu_seed.hex()}')

    wifi_seed = get_wifi_seed(num_bytes=64//3)
    print(f'wifi_seed: {wifi_seed.hex()}')

    weather_seed = get_weather_seed(num_bytes=64//3)
    print(f'weather_seed: {weather_seed.hex()}')

    random.seed(cpu_seed + wifi_seed + weather_seed)

    rand_ints = [random.randint(1,100) for _ in range(10)]
    print(f'rand_ints: {rand_ints}')
