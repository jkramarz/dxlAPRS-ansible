#!/usr/bin/env python3
import subprocess
import re
from functools import reduce
import sys
import argparse

def get_channels(band="GSM900", timeout=60):
    output = subprocess.check_output(['/usr/local/bin/kal', '-s', band], timeout=timeout)
    match = re.finditer('chan: (?P<channel>[\d]+) \(.*\) power: (?P<power>[\d.]+)', str(output))
    return map(
        lambda x: x.groupdict(),
        match
    )

def get_strongest_channel(channels):
    return reduce(
        lambda carry, item: carry if float(item['power']) < float(carry['power']) else item,
        channels
    )

def calibrate(channel_number, timeout=60):
    output = subprocess.check_output(['/usr/local/bin/kal', '-c', channel_number], timeout=timeout)
    match = re.search('average absolute error: (?P<ppm>[\d.\-]+) ppm', str(output))
    return match.groupdict()['ppm']

parser = argparse.ArgumentParser(description='Get RTLSDR calibration PPM.')
parser.add_argument('band', type=str, nargs='?', help='GSM band to scan', default="GSM900", choices=['GSM850', 'GSM-R', 'GSM900', 'EGSM', 'DCS', 'PCS'])
parser.add_argument('--config', type=str, help='Configuration file to write result')
args = parser.parse_args()

try:
    channels = get_channels(args.band)
    strongest = get_strongest_channel(channels)
    ppm = calibrate(strongest['channel'])
    if args.config:
        with open(args.config, 'w') as f:
            f.write("PPM=%s\n" % ppm)
    else:
        print(ppm)
    sys.exit(0)
except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)
