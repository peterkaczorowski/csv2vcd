# CSV to VCD Converter

A simple Python script to convert digital logic signal data from CSV files into VCD (Value Change Dump) format.
This allows viewing and analyzing signal waveforms in standard waveform viewers.

## Features

- Reads CSV files containing time in seconds and digital signal values (0 or 1).
- Converts time units from seconds to microseconds for VCD format.
- Outputs VCD files compatible with common waveform analysis tools.
- Supports multiple signals, tracking and writing only value changes to minimize file size.
- Skips duplicate time entries to ensure clean waveform data.
- Allows specifying the output timescale via a command-line switch (e.g., -t 10ps, -t 1us).

## CSV Input Format

The CSV file should have a header with the following structure:

Time [s], Signal1, Signal2, Signal3, ...

0.000000, 0, 1, 0, ...

0.000001, 1, 1, 0, ...

...

## Timescale Option
The script supports a -t command-line option to specify the timescale unit used in the output VCD file. The timescale controls the granularity of the time values in the VCD and must be provided as a number followed by a time unit. Supported units are:

- ps — picoseconds
- ns — nanoseconds
- us — microseconds (default)
- ms — milliseconds

Examples of usage:

python csv_to_vcd.py -t 10ps input.csv output.vcd

python csv_to_vcd.py -t 1ns input.csv output.vcd

python csv_to_vcd.py input.csv output.vcd   # uses default timescale 1 us


## Notes
This program can be used to convert CSV data exported from Saleae Logic software (versions 1.x and 2.x) after logic signal acquisition.
The resulting VCD file can then be loaded into waveform viewers such as PulseView or imported into simulation tools for further analysis.

If you want to further use the data in a program like Active HDL (even the student version), the **vcd2asdb** program is needed. It is available in the Aldec Riviera Pro package.

## Dependencies

1. Python 3.x (tested with Python 3.12.7)
2. pyvcd library (install via pip: `pip install pyvcd`)

## License

This project is licensed under the GNU General Public License v3.0 (GPLv3).

You are free to use, modify, and distribute this software under the terms of the GPLv3 license.

For the full license text, see the `LICENSE` file included in this repository.


