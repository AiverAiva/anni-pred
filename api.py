from fastapi import FastAPI, HTTPException
import json
from datetime import datetime, timezone
import httpx
import os 

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

STABLE_JSON_PATH = "data/stable.json"
GITHUB_API_URL = "https://api.github.com/repos/AiverAiva/anni-pred/actions/workflows/run_prediction.yml/dispatches"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Use an environment variable

if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN environment variable is not set")

@app.get("/")
async def check_and_dispatch():
    try:
        with open(STABLE_JSON_PATH, "r") as f:
            stable_data = json.load(f)
        
        current_timestamp_ms = stable_data["current"]["datetime_utc"]
        current_datetime = datetime.fromtimestamp(current_timestamp_ms / 1000, tz=timezone.utc)
        
        now = datetime.now(timezone.utc)
        if now < current_datetime:
            return {"message": "The time has not passed yet"}
        
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        payload = {"ref": "main"}  
        
        async with httpx.AsyncClient() as client:
            response = await client.post(GITHUB_API_URL, headers=headers, json=payload)
        
        if response.status_code == 204:
            return {"message": "Workflow dispatched successfully"}
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
