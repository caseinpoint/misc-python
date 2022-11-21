from json import loads
import random
from re import compile, IGNORECASE
from secrets import choice
from subprocess import run

RE_SIGNAL = compile(r'Signal level=(?P<signal>-\d+)', IGNORECASE)
# RE_ADDRESS = compile(r'Address:\s*(?P<address>\S+)', IGNORECASE)
# RE_CHANNEL = compile(r'Channel:\s*(?P<channel>\d+)', IGNORECASE)
# RE_QUAL_SIG = compile(r'Quality=(?P<quality>\d+)/70\s+Signal level=(?P<signal>-\d+)', IGNORECASE)
# RE_BEACON = compile(r'Last beacon:\s+(?P<beacon>\d+)', IGNORECASE)


def get_wifi_seed(num_bytes=64):
    wifi_scan_result = run(['sudo', 'iwlist', 'scan'],
                           capture_output=True,
                           encoding='locale')

    signals = RE_SIGNAL.findall(wifi_scan_result.stdout)

    signal_choice = choice(signals)

    random.seed(hash(signal_choice))

    return random.randbytes(num_bytes)


def extract_inputs(input_dict, results=[]):
    """Recursively extract all non-zero values where key ends with '_input'."""

    for key, val in input_dict.items():
        if isinstance(val, dict):
            extract_inputs(val, results)
        elif key.endswith('_input') and val != 0:
            results.append(val)

    return results


def get_cpu_seed(num_bytes=64):
    cpu_result = run(['sensors', '-j'],
                     capture_output=True,
                     encoding='locale')
    json_result = loads(cpu_result.stdout)

    inputs = extract_inputs(json_result)

    sensor_choice = str(choice(inputs))

    random.seed(hash(sensor_choice))

    return random.randbytes(num_bytes)


if __name__ == '__main__':
    print('test output:')

    cpu_seed = get_cpu_seed(num_bytes=32)
    print(f'cpu_seed: {cpu_seed.hex()}')

    wifi_seed = get_wifi_seed(num_bytes=32)
    print(f'wifi_seed: {wifi_seed.hex()}')

    random.seed(cpu_seed + wifi_seed)

    rand_ints = [random.randint(1,100) for _ in range(10)]
    print(f'rand_ints: {rand_ints}')
