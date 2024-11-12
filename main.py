import json
import os
import datetime
import subprocess

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def append_to_history(history_file, timestamp):
    history = load_json(history_file) or []
    if {"datetime_utc": timestamp} not in history:
        history.append({"datetime_utc": timestamp})
    save_json(history_file, history)

def update_stable_json(stable_file, history_file):
    stable = load_json(stable_file) or {"current": {}, "predicted": []}
    history = load_json(history_file) or []
    current_time = datetime.datetime.now().timestamp() * 1000

    if "datetime_utc" in stable["current"]:
        current_timestamp = stable["current"]["datetime_utc"]
        is_predicted = stable["current"].get("predicted", False)

        if not is_predicted:
            if {"datetime_utc": current_timestamp} not in history:
                append_to_history(history_file, current_timestamp)
        if current_timestamp < current_time:
            stable["current"] = {}

    if not stable["current"]:
        if stable["predicted"]:
            stable["current"] = stable["predicted"].pop(0)
        save_json(stable_file, stable)

def fill_closest_predictions(stable_file, predicted_file):
    stable = load_json(stable_file) or {"current": {}, "predicted": []}
    predicted_data = load_json(predicted_file) or []
    current_time = datetime.datetime.now().timestamp() * 1000

    future_predictions = sorted(
        [item for item in predicted_data if item["datetime_utc"] > current_time],
        key=lambda x: x["datetime_utc"]
    )

    stable["predicted"] = future_predictions[:5]

    if "datetime_utc" in stable["current"]:
        current_timestamp = stable["current"]["datetime_utc"]
        first_predicted_timestamp = stable["predicted"][0]["datetime_utc"]

        time_difference_days = (first_predicted_timestamp - current_timestamp) / (24 * 3600 * 1000)
        
        if time_difference_days < 3 and len(future_predictions) > 5:
            stable["predicted"] = future_predictions[1:6]

    save_json(stable_file, stable)

# Main execution
stable_file = './data/stable.json'
history_file = './data/history.json'
predicted_file = './data/predicted.json'

update_stable_json(stable_file, history_file)

subprocess.run(['python', 'pred.py'])

fill_closest_predictions(stable_file, predicted_file)

subprocess.run(['python', 'generate_cronjob.py'])
