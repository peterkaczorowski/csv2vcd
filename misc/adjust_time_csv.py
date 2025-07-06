"""
Adjust time: shift all timestamps so that the first one starts at 0 seconds
Code written by Piotr D. Kaczorowski
"""

import csv
import sys

def adjust_time(input_file, output_file):
    with open(input_file, 'r', newline='') as infile:
        reader = list(csv.reader(infile))
        header = reader[0]
        data = reader[1:]

        if not data:
            print("No data in the file.")
            return

        # Read the first timestamp from the data
        first_time = float(data[0][0])

        # Modify times and store adjusted data
        adjusted_data = []
        for row in data:
            adjusted_row = [f"{float(row[0]) - first_time:.9f}"] + row[1:]
            adjusted_data.append(adjusted_row)

    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)
        writer.writerows(adjusted_data)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python adjust_time_csv.py input.csv output.csv")
        sys.exit(1)

    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    adjust_time(input_csv, output_csv)

