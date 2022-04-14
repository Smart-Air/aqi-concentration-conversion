import argparse
from aqi_conversions import *
import sys

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--test', dest='test', action='store_true',
                    default=False,
                    help='run unit tests')
parser.add_argument('--aqi', dest='from_aqi', action='store_true',
                    default=False,
                    help='convert from aqi (default is to use US AQI, unless --standard <other> is passed)')
parser.add_argument('--conc', dest='from_conc', action='store_true',
                    default=False,
                    help='convert from concentration to AQI (default is to use US AQI, unless --standard <other> is passed)')
parser.add_argument('values', metavar='conc/AQI', type=float, nargs='?',
                    help='A concentration value to convert to AQI')
parser.add_argument('--from_file', dest="from_file", nargs=1)
parser.add_argument('--standard', dest="standard", nargs=1)

class IllegalArgumentError(ValueError):
    pass


def convert(val, standard, from_conc):
    if standard == 'us':
        if from_conc:
            return concentration_to_us_aqi(val)
        else:
            return us_aqi_to_china_aqi(val)
    elif standard == 'china':
        if from_conc:
            return concentration_to_china_aqi(val)
        else:
            return china_aqi_to_concentration(val)

if __name__ == "__main__":
    args = parser.parse_args()
    if args.test:
        unittest.main()
        sys.exit()
    if args.standard:
        standard = args.standard[0].lower()
        if standard not in ['china', 'us']:
            raise IllegalArgumentError("Currently only US and China standards are supported")
    else:
        # default to US
        standard = 'us'


    if args.from_file:
        for f in args.from_file:
            with open(f) as ff:
                lines = [float(ll.strip()) for l in ff.readlines() for ll in l.strip().split("\r")]
            for l in lines:
                convert(l, standard, args.from_conc)
                    
    else:
        if not args.values:
            raise IllegalArgumentError("You must provide at least one value to convert")
        for val in [args.values]:
            print convert(val, standard, args.from_conc)
