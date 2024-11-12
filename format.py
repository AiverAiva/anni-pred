# from datetime import datetime
import json
import os
# dt = datetime.fromisoformat(input().replace("Z", "+00:00"))
# # Convert datetime to UTC timestamp in milliseconds
# print(int(dt.timestamp() * 1000))\
    
def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
        
file = './data/history.json'
fileData = load_json(file)

fileData.sort(key=lambda x: x["datetime_utc"])
save_json(file, fileData)