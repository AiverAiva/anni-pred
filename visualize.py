import json
import os
from datetime import datetime

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def format_timestamp(timestamp):
    """Convert a Unix timestamp in milliseconds to a human-readable date."""
    return datetime.utcfromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S UTC')

def display_stable_data(stable_file):
    stable_data = load_json(stable_file)
    if not stable_data:
        print("No data found in stable.json")
        return

    print("=== Stable Data ===")
    if 'current' in stable_data and 'datetime_utc' in stable_data['current']:
        print("Current Event:")
        print(f"  DateTime: {format_timestamp(stable_data['current']['datetime_utc'])}")
    else:
        print("Current Event: None")

    # Display predicted events in stable.json
    print("\nPredicted Events:")
    for event in stable_data.get('predicted', []):
        date_str = format_timestamp(event['datetime_utc'])
        predicted_status = event.get('predicted', False)
        print(f"  DateTime: {date_str} | Predicted: {predicted_status}")

def display_history_data(history_file):
    history_data = load_json(history_file)
    if not history_data:
        print("No data found in history.json")
        return

    print("\n=== History Data ===")
    for event in history_data:
        if 'datetime_utc' in event:
            print(f"  DateTime: {format_timestamp(event['datetime_utc'])}")

# File paths
stable_file = './data/stable.json'
history_file = './data/history.json'
predicted_file = './data/predicted.json'
# Display data
display_stable_data(stable_file)
display_history_data(history_file)
display_history_data(predicted_file)
