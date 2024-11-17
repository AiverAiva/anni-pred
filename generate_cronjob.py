import json
from datetime import datetime
from pathlib import Path

# File paths
STABLE_PATH = Path("data/stable.json")
VERCEL_CONFIG_PATH = Path("vercel.json")

def convert_to_cron(timestamp_ms):
    """
    Convert a timestamp in milliseconds to a cron expression.
    """
    dt = datetime.utcfromtimestamp(timestamp_ms / 1000)
    cron_expression = f"{dt.minute+1} {dt.hour} {dt.day} {dt.month} *"
    return cron_expression

def update_vercel_config(cron_expression):
    """
    Update the Vercel configuration file with the new cron schedule.
    """
    if not VERCEL_CONFIG_PATH.exists():
        # If the file doesn't exist, create a basic structure
        vercel_config = {
            "builds": [
                {
                    "src": "api.py",
                    "use": "@vercel/python"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "api.py"
                }
            ]
            ,
            "crons": []
        }
        
    else:
        with open(VERCEL_CONFIG_PATH, "r") as file:
            vercel_config = json.load(file)

    cron_entry = {
        "path": "/",
        "schedule": cron_expression
    }

    vercel_config["crons"] = [entry for entry in vercel_config.get("crons", []) if entry["path"] != "/"]
    vercel_config["crons"].append(cron_entry)

    with open(VERCEL_CONFIG_PATH, "w") as file:
        json.dump(vercel_config, file, indent=4)
    
    print(f"Vercel configuration updated with cron schedule: {cron_expression}")

def main():
    """
    Main function to read stable.json, generate cron expression, and update vercel.json.
    """
    with open(STABLE_PATH, "r") as file:
        data = json.load(file)

    current_timestamp_ms = data["current"]["datetime_utc"]

    cron_expression = convert_to_cron(current_timestamp_ms)

    update_vercel_config(cron_expression)

if __name__ == "__main__":
    main()
