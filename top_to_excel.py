import pandas as pd
import os
import datetime

# Get current timestamp
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Run 'top' command and capture output
top_output = os.popen("top -b -n 1").read().splitlines()

# Extract relevant data (Skip headers and unwanted data)
data = []
for line in top_output:
    if line.startswith("PID") or not line.strip():  # Skip header or empty lines
        continue
    
    parts = line.split()
    
    # Ensure valid data has enough columns (processes should have at least 12 parts)
    if len(parts) < 12:
        continue
    
    # Only consider lines that are actual processes, avoiding system/kernel processes with no user data
    if parts[1] == 'root' or parts[1] == 'USER':  # Skip root/USER or kernel processes
        continue

    data.append([current_time, parts[0], parts[1], parts[8], parts[9], parts[11]])

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Timestamp", "PID", "USER", "CPU%", "MEM%", "COMMAND"])

# Append data instead of overwriting (Keep historical records)
filename = "system_usage.xlsx"

try:
    existing_df = pd.read_excel(filename)  # Load existing file
    df = pd.concat([existing_df, df], ignore_index=True)  # Append new data
except FileNotFoundError:
    pass  # If file doesn't exist, it will be created

# Save the updated data
df.to_excel(filename, index=False)

print(f"Excel file '{filename}' updated successfully with new timestamped data!")
