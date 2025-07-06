"""
This script merges two CSV files containing CSYNC and VSYNC signal data,
each sampled at different timestamps. The goal is to produce a unified timeline
that aligns both datasets, allowing for signal comparison and analysis.

How it works:
- Each input CSV file contains 'Time [s]', 'CSYNC', and 'VSYNC' columns.
- Timestamps are rounded to 9 decimal places for consistency.
- Signal columns are renamed (CSYNC_A, VSYNC_A, CSYNC_B, VSYNC_B) to distinguish sources.
- The files are merged using an outer join on 'Time [s]' to include all time points.
- Missing values are forward-filled (ffill) to carry over the last known signal state.
- Any remaining NaNs (before the first known value) are filled with 0.
- Signal columns are converted to integers; timestamps remain as high-precision floats.
- The final merged data is saved to an output CSV file.

This technique is useful for synchronizing asynchronous signal recordings and
ensuring a complete timeline with minimal data loss.

Usage:
    python merge_csync_vsync.py input1.csv input2.csv output.csv

Code written by Piotr D. Kaczorowski
"""


import pandas as pd
import sys

def merge_csync_vsync(file1, file2, output):
    # Load only the required columns
    df1 = pd.read_csv(file1, usecols=['Time [s]', 'CSYNC', 'VSYNC'])
    df2 = pd.read_csv(file2, usecols=['Time [s]', 'CSYNC', 'VSYNC'])

    # Round time to 9 decimal places to facilitate merging
    df1['Time [s]'] = df1['Time [s]'].round(9)
    df2['Time [s]'] = df2['Time [s]'].round(9)

    # Rename CSYNC and VSYNC columns to distinguish the source
    df1 = df1.rename(columns={'CSYNC': 'CSYNC_A', 'VSYNC': 'VSYNC_A'})
    df2 = df2.rename(columns={'CSYNC': 'CSYNC_B', 'VSYNC': 'VSYNC_B'})

    # Merge data on the time column (outer join)
    merged = pd.merge(df1, df2, on='Time [s]', how='outer')

    # Sort by time
    merged = merged.sort_values('Time [s]').reset_index(drop=True)

    # Forward fill missing values
    merged = merged.ffill()

    # Fill any remaining NaNs at the beginning with zeros
    merged = merged.fillna(0)

    # Convert types: time to float, the rest to int
    merged['Time [s]'] = merged['Time [s]'].astype(float)
    merged['CSYNC_A'] = merged['CSYNC_A'].astype(int)
    merged['VSYNC_A'] = merged['VSYNC_A'].astype(int)
    merged['CSYNC_B'] = merged['CSYNC_B'].astype(int)
    merged['VSYNC_B'] = merged['VSYNC_B'].astype(int)

    # Save to file with 9 decimal places of precision for time
    merged.to_csv(output, index=False, float_format='%.9f')

    print(f"Merged file saved to {output}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python merge_csync_vsync.py input1.csv input2.csv output.csv")
        sys.exit(1)

    merge_csync_vsync(sys.argv[1], sys.argv[2], sys.argv[3])

