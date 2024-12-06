from datetime import datetime, timedelta
import pandas as pd

# Function to check if a day is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # Saturday (5) and Sunday (6)

# Function to schedule upgrades
def schedule_upgrades(data, start_date, max_nodes_per_day=6):
    timeline = []
    current_date = start_date

    # Process each street sequentially
    for street, group in data.groupby('street'):
        masters = group[group['Type'].str.contains('master')].sort_values(by='Oneview Node')
        workers = group[group['Type'].str.contains('worker')].sort_values(by='Oneview Node')
        
        master_nodes = masters['Oneview Node'].tolist()
        worker_nodes = workers['Oneview Node'].tolist()
        remaining_workers = set(worker_nodes)

        while master_nodes or remaining_workers:
            # Skip weekends
            while is_weekend(current_date):
                current_date += timedelta(days=1)

            daily_schedule = []

            # Schedule master nodes (one per day)
            if master_nodes and len(daily_schedule) < max_nodes_per_day:
                daily_schedule.append(master_nodes.pop(0))

            # Schedule worker nodes (fill remaining slots)
            if remaining_workers:
                remaining_slots = max_nodes_per_day - len(daily_schedule)
                if remaining_slots > 0:
                    to_schedule = list(remaining_workers)[:remaining_slots]
                    daily_schedule.extend(to_schedule)
                    remaining_workers.difference_update(to_schedule)

            # Ensure at least one worker remains running
            if len(daily_schedule) >= len(worker_nodes) - 1 and len(daily_schedule) > 0:
                last_worker = daily_schedule.pop()
                remaining_workers.add(last_worker)

            # Record schedule for the day
            for node in daily_schedule:
                node_type = group[group['Oneview Node'] == node]['Type'].values[0]
                timeline.append({
                    'Oneview Node': node,
                    'Type': node_type,
                    'street': street,
                    'Upgrade Date': current_date.strftime('%Y-%m-%d')
                })

            # Move to the next day
            current_date += timedelta(days=1)

    return pd.DataFrame(timeline)

# Input file path
file_path = 'node_data.txt'

# Read data from the file
df = pd.read_csv(file_path, sep="\t")

# Generate the upgrade timeline
start_date = datetime(2025, 2, 20)
timeline_df = schedule_upgrades(df, start_date)

# Display the timeline
print(timeline_df)

# Optionally, save the timeline to a file
output_file = 'upgrade_timeline.csv'
timeline_df.to_csv(output_file, index=False)
print(f"Upgrade timeline saved to {output_file}")

