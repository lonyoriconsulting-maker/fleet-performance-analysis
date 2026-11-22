# Fleet Performance Analysis

A lightweight Python script that analyses fleet telematics data to surface vehicle performance, driver safety scores, and fuel anomalies — built as a practical demonstration of fleet operations analytics.

## What it does

- Computes per-vehicle summary statistics (distance, fuel efficiency, idle time)
- Calculates driver safety scores based on speeding and harsh-braking events
- Flags anomalies consistent with fuel siphoning or abnormal consumption
- Outputs a clean text report to the terminal

## Sample output

=== VEHICLE SUMMARY ===
T 123 ABC | Distance: 1,240 km | Efficiency: 8.2 km/L | Idle: 3.5 hrs

=== DRIVER SAFETY SCORES ===
Driver J. Mwita | Score: 87/100 | Events: 2 speeding, 1 harsh brake

=== ANOMALY FLAGS ===
T 456 DEF | Fuel drop detected: -42L over 6 hrs | Flag: POSSIBLE SIPHONING

## How to run

Requires Python 3.8+ and pandas.

```bash
pip install pandas
python fleet_analysis.py
The script reads fleet_data.csv from the same directory.

Data

fleet_data.csv contains 12 sample records with 8 columns covering vehicle ID, distance, fuel consumed, idle time, speeding events, harsh braking events, and timestamps.

Author

Lonyori Ole Meiludie — Fleet & Logistics Operations Manager with data automation expertise.
LinkedIn: https://www.linkedin.com/in/lonyori-ole-meilud24/ | GitHub: https://github.com/lonyoriconsulting-maker
