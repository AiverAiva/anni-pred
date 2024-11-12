import json
from datetime import datetime
from pathlib import Path

# File paths
STABLE_PATH = Path("data/stable.json")
CRONJOB_PATH = Path("data/cronjob.json")

def convert_to_cron(timestamp_ms):
    # Convert timestamp from milliseconds to a datetime object
    dt = datetime.utcfromtimestamp(timestamp_ms / 1000)
    
    # Create a cron expression in the format: "minute hour day month *"
    cron_expression = f"{dt.minute} {dt.hour} {dt.day} {dt.month} *"
    
    return cron_expression

def create_cronjob_file():
    # Load the predicted JSON data
    with open(STABLE_PATH, "r") as file:
        data = json.load(file)
    
    # Extract the current datetime in milliseconds
    current_timestamp_ms = data["current"]["datetime_utc"]
    
    # Convert to cron format
    cron_expression = convert_to_cron(current_timestamp_ms)
    
    # Create the cronjob JSON structure
    cronjob_data = {
        "datetime_cron": cron_expression
    }
    
    # Save the cron expression to cronjob.json
    with open(CRONJOB_PATH, "w") as file:
        json.dump(cronjob_data, file, indent=4)
    
    print(f"Cronjob saved in {CRONJOB_PATH}")

# Run the function
create_cronjob_file()
