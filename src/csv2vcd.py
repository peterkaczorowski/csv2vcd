"""
CSV to VCD converter
Code written by Piotr D. Kaczorowski
"""

import csv
import sys
from vcd import VCDWriter

def csv_to_vcd(csv_filename, vcd_filename, timescale='1 us'):
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        signals = reader.fieldnames[1:]  # skip the "Time [s]" column

        ids = [chr(i) for i in range(33, 33 + len(signals))]

        with open(vcd_filename, 'w') as vcdfile:
            with VCDWriter(vcdfile, timescale=timescale, date='today', comment='CSV to VCD conversion') as writer:
                signal_vars = {}
                for name, id_ in zip(signals, ids):
                    signal_vars[name] = writer.register_var('top', name, 'wire', size=1)

                for row in reader:
                    time_s = float(row['Time [s]'])

                    # Parse the timescale string, e.g. '10ps', into number and unit parts'
                    scale_num = int(''.join(filter(str.isdigit, timescale)))
                    scale_unit = ''.join(filter(str.isalpha, timescale)).lower()

                    # Convert time from seconds to the VCD timescale units
                    if scale_unit == 'ps':
                        time_vcd = int(time_s * 1e12 / scale_num)
                    elif scale_unit == 'ns':
                        time_vcd = int(time_s * 1e9 / scale_num)
                    elif scale_unit == 'us':
                        time_vcd = int(time_s * 1e6 / scale_num)
                    elif scale_unit == 'ms':
                        time_vcd = int(time_s * 1e3 / scale_num)
                    else:
                        # Default to microseconds if unit is unrecognized
                        time_vcd = int(time_s * 1e6)

                    for name in signals:
                        value = row[name]
                        writer.change(signal_vars[name], time_vcd, int(value))

def print_usage():
    print("Usage: csv2vcd [-t TIMESCALE] input.csv output.vcd")
    print("Example timescale values: 1us, 10ps, 100ns")

if __name__ == '__main__':
    args = sys.argv[1:]
    timescale = '1 us'
    if '-t' in args:
        t_index = args.index('-t')
        if t_index + 1 < len(args):
            timescale = args[t_index + 1]
            # Remove '-t' and its argument from args
            args.pop(t_index + 1)
            args.pop(t_index)
        else:
            print("Error: -t requires an argument")
            print_usage()
            sys.exit(1)

    if len(args) != 2:
        print_usage()
        sys.exit(1)

    csv_to_vcd(args[0], args[1], timescale)

