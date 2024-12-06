from datetime import datetime, timedelta
from calendar import monthcalendar, TextCalendar
import pandas as pd

# Function to read input data from a text file
def read_node_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    headers = lines[0].split()
    rows = [line.split(maxsplit=1) for line in lines[1:]]
    df = pd.DataFrame(rows, columns=headers)
    # Clean whitespace and newline characters
    df['Node'] = df['Node'].str.strip()
    df['Type'] = df['Type'].str.strip()
    return df

# Function to check if a day is a weekend
def is_weekend(date):
    return date.weekday() >= 5  # Saturday (5) and Sunday (6)

# Function to generate a calendar with nodes listed for each date
def generate_calendar_with_nodes(timeline, year, month):
    cal = TextCalendar()
    month_days = monthcalendar(year, month)
    calendar_output = []
    for week in month_days:
        week_output = []
        for day in week:
            if day == 0:
                week_output.append("   ")  # Empty days in the calendar
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                nodes_on_date = timeline[timeline["Upgrade Date"] == date_str]["Node"].tolist()
                if nodes_on_date:
                    nodes_str = ", ".join(nodes_on_date)
                    week_output.append(f"{day:2d}*")  # Mark days with upgrades
                else:
                    week_output.append(f"{day:2d} ")
        calendar_output.append(" ".join(week_output))
    return "\n".join(calendar_output)

# Function to display nodes for each date below the calendar
def display_nodes_per_date(timeline):
    nodes_per_date = {}
    for _, row in timeline.iterrows():
        date = row["Upgrade Date"]
        node = row["Node"]
        node_type = row["Type"]
        if date not in nodes_per_date:
            nodes_per_date[date] = []
        nodes_per_date[date].append(f"{node} ({node_type})")
    
    output = []
    for date, nodes in sorted(nodes_per_date.items()):
        output.append(f"{date}: {', '.join(nodes)}")
    return "\n".join(output)

# Input file path (assume file named 'node_data.txt')
file_path = 'node_data.txt'

# Read data from the file
df = read_node_data(file_path)

# Categorize nodes into groups
masters = df[df['Type'].str.contains('master')]['Node'].tolist()
workers = df[df['Type'].str.contains('worker')]['Node'].tolist()

# Initialize timeline parameters
start_date = datetime(2025, 2, 21)
nodes_per_day = 6
timeline = []

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

# Create a timeline DataFrame for output and merge with node types
timeline_df = pd.DataFrame(timeline)
timeline_df = timeline_df.merge(df, on="Node")

# Generate calendar and list of nodes per date
calendar_output = generate_calendar_with_nodes(timeline_df, 2025, 1)
nodes_per_date_output = display_nodes_per_date(timeline_df)

# Display the results
print("Node Types Table:")
print(df)
print("\nNode Upgrade Timeline (Date per Node and Type):")
print(timeline_df)
print("\nUpgrade Calendar for January 2025:")
print(calendar_output)
print("\nNodes Scheduled for Each Date:")
print(nodes_per_date_output)
