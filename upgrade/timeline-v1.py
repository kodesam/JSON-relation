from datetime import datetime, timedelta
import pandas as pd

# Input data
data = """
Node            Type
nodest1rm016    control-plane,master
nodest1rm017    control-plane,master
nodest1rm018    control-plane,master
nodest1rm019    worker,worker-nokia
nodest1rm020    worker,worker-nokia
nodest1rm021    worker,worker-nokia
nodest1rm022    worker,worker-nokia
nodest1rm023    worker,worker-nokia-cmg
nodest1rm025    worker,worker-nokia-cmg
nodest1rm026    worker,worker-nokia-cmg
nodest1rm027    worker,worker-nokia-ht
nodest1rm028    worker,worker-nokia-ht
nodest1rm029    worker,worker-nokia-ht
nodest1rm030    worker,worker-nokia-ht
nodest1rm031    worker,worker-nokia-ht
nodest1rm032    worker,worker-nokia-ht
nodest1rm049    worker,worker-nokia-ht
nodest1rm050    worker,worker-nokia-ht
nodest1rm051    worker,worker-nokia-ht
nodest1rm052    worker,worker-nokia
nodest1rm059    worker,worker-nokia
nodest1rm060    worker,worker-nokia-ncc
nodest1rm061    worker,worker-nokia-ncc
nodest1rm062    worker,worker-nokia-ncc
nodest1rm063    worker,worker-nokia-ncc
"""

# Parse input data into a DataFrame
lines = data.strip().split("\n")
headers = lines[0].split()
rows = [line.split(maxsplit=1) for line in lines[1:]]
df = pd.DataFrame(rows, columns=headers)

# Categorize nodes into groups
masters = df[df['Type'].str.contains('master')]['Node'].tolist()
workers = df[df['Type'].str.contains('worker')]['Node'].tolist()

# Initialize timeline parameters
start_date = datetime(2025, 1, 15)
nodes_per_day = 6
timeline = []

# Function to check if a day is a weekend
def is_weekend(date):
    return date.weekday() >= 5

# Schedule nodes
remaining_workers = set(workers)
current_date = start_date

while masters or remaining_workers:
    # Skip weekends
    while is_weekend(current_date):
        current_date += timedelta(days=1)
    
    daily_schedule = []
    
    # Schedule masters (one per day)
    if masters:
        daily_schedule.append(masters.pop(0))
    
    # Schedule workers (up to remaining slots)
    if remaining_workers:
        remaining_slots = nodes_per_day - len(daily_schedule)
        if remaining_slots > 0:
            to_schedule = list(remaining_workers)[:remaining_slots]
            daily_schedule.extend(to_schedule)
            remaining_workers.difference_update(to_schedule)
    
    # Ensure at least one worker remains un-upgraded
    if len(daily_schedule) >= len(workers) - 1 and len(daily_schedule) > 0:
        last_worker = daily_schedule.pop()
        remaining_workers.add(last_worker)
    
    # Add the schedule for the day
    for node in daily_schedule:
        timeline.append({'Node': node, 'Upgrade Date': current_date.strftime('%Y-%m-%d')})
    
    # Move to the next day
    current_date += timedelta(days=1)

# Create a timeline DataFrame for output
timeline_df = pd.DataFrame(timeline)

timeline_df
