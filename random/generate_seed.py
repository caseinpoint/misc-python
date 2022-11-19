from json import loads
import random
from re import compile, IGNORECASE
from secrets import choice
from subprocess import run

RE_ADDRESS = compile(r'Address:\s*(?P<address>\S+)', IGNORECASE)
RE_SIGNAL = compile(r'Signal level=(?P<signal>-\d+)', IGNORECASE)
# RE_CHANNEL = compile(r'Channel:\s*(?P<channel>\d+)', IGNORECASE)
# RE_QUAL_SIG = compile(r'Quality=(?P<quality>\d+)/70\s+Signal level=(?P<signal>-\d+)', IGNORECASE)
# RE_BEACON = compile(r'Last beacon:\s+(?P<beacon>\d+)', IGNORECASE)


def get_wifi_seed(start_seed=None):
    """Return a randomly chosen nearby wifi address for use as seed."""

    wifi_scan_result = run(['sudo', 'iwlist', 'scan'],
                           capture_output=True,
                           encoding='locale')

    signals = RE_SIGNAL.findall(wifi_scan_result.stdout)

    addresses = RE_ADDRESS.findall(wifi_scan_result.stdout)
    # print(f'# wifi results: {len(addresses)}')

    # choose a signal strength for 1st seed
    if start_seed is None:
        # cryptographically strong secrets.choice
        signal_choice = choice(signals)
    else:
        random.seed(start_seed)
        signal_choice = random.choice(signals)
    # print(f'signal choice: {signal_choice} (idx: {signals.index(signal_choice)})')

    # use 1st seed to pseudorandomly choose an address for result seed
    random.seed(signal_choice)

    address_choice = random.choice(addresses)
    # print(f'address choice: {address_choice} (idx: {addresses.index(address_choice)})')

    return address_choice


def extract_inputs(input_dict, results=[]):
    """Recursively extract all non-zero values where key ends with '_input'."""

    for key, val in input_dict.items():
        if isinstance(val, dict):
            extract_inputs(val, results)
        elif key.endswith('_input') and val != 0:
            results.append(val)

    return results


def get_cpu_seed(start_seed=None):
    """Return a randomly chosen temp or fan speed for use as seed."""

    cpu_result = run(['sensors', '-j'],
                     capture_output=True,
                     encoding='locale')
    json_result = loads(cpu_result.stdout)

    inputs = extract_inputs(json_result)

    if start_seed is None:
        # cryptographically strong secrets.choice
        sensor_choice = choice(inputs)
    else:
        random.seed(start_seed)
        sensor_choice = random.choice(inputs)
    # print(f'sensor choice: {sensor_choice} (idx: {inputs.index(sensor_choice)})')

    return sensor_choice


if __name__ == '__main__':
    print('test output:')

    cpu_seed = get_cpu_seed()
    print(f"cpu_seed: '{cpu_seed}'", end=' ')

    wifi_seed = get_wifi_seed(start_seed=cpu_seed)
    print(f"wifi_seed: '{wifi_seed}'")

    random.seed(wifi_seed)

    rand_ints = [random.randint(1,100) for _ in range(10)]
    print(f'rand_ints: {rand_ints}')