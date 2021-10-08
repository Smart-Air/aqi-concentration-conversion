import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--aqi', dest='from_aqi', action='store_true',
                    default=False,
                    help='sum the integers (default: find the max)')
parser.add_argument('--conc', dest='from_conc', action='store_true',
                    default=False,
                    help='sum the integers (default: find the max)')
parser.add_argument('values', metavar='conc/AQI', type=float, nargs='?',
                    help='A concentration value to convert to AQI')
parser.add_argument('--from_file', dest="from_file", nargs=1)

def get_vals(reverse=False):
    aqi_conc = []
    with open('AQI-to-Conc.csv', 'r') as w:
        lines = [l.strip() for l in w.readlines()]
    for l in lines:
        aqi, conc = [float(a) for a in l.split(",")]
        aqi_conc.append((conc, aqi) if reverse is True else (aqi, conc))
    return aqi_conc

AQI_TO_CONC = get_vals()
CONC_TO_AQI = get_vals(reverse=True)

def interpolate(val, vals):
    for i, (x, y) in enumerate(vals):
        if x < val:
            continue
        x_1, y_1 = vals[i-1]
        return y + float(val - x)/(x - x_1)*(y - y_1)

def conc_to_aqi(conc, print_screen=True):
    val = interpolate(conc, CONC_TO_AQI)
    if (print_screen):
        print("Conc: %s" % conc, "/ AQI: %.1f" % val)
    else:
        return val


def aqi_to_conc(aqi, print_screen=True):
    val = interpolate(aqi, AQI_TO_CONC)
    if (print_screen):
        print("AQI: %s" % aqi, "/ Conc: %.1f" % val)
    else:
        return val
        
if __name__ == "__main__":
    args = parser.parse_args()
    if args.from_file:
        vals = get_vals(reverse=args.from_conc)
        for f in args.from_file:
            with open(f) as ff:
                lines = [float(ll.strip()) for l in ff.readlines() for ll in l.strip().split("\r")]
            for l in lines:
                print("%s" % interpolate(l, vals))
    else:
        for val in [args.values]:
            if args.from_conc:
                conc_to_aqi(val)
            elif args.from_aqi:
                aqi_to_conc(val)
