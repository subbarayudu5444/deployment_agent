from fastapi import FastAPI, HTTPException
import requests
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

RENDER_API_KEY = os.getenv("RENDER_API_KEY")
@app.get("/")
async def root():
    return {"message": "Hello, Welcome to coastal Seven"}
@app.post("/deploy")
async def deploy_repository(repo_url: str):
    """Deploy a GitHub repository to Render."""
    try:
        # Validate GitHub repository URL
        if not repo_url.startswith("https://github.com/"):
            raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

        # Extract repository name
        repo_name = repo_url.split("/")[-1].replace(".git", "")

        # Render API URL and headers
        render_api_url = "https://api.render.com/v1/services"
        headers = {
            "Authorization": f"Bearer {RENDER_API_KEY}",
            "Content-Type": "application/json"
        }

        # Payload for creating a new web service
        payload = {
            "type": "web_service",
            "name": repo_name,
            "ownerId": "tea-d2i4gdje5dus73ed5oag",
            "repo": repo_url,
            "branch": "main",
            "buildCommand": "cd backend && pip install -r requirements.txt",
            "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port 10000",
            "envVars": [],
            "serviceDetails": {
                "env": "python3",
                "region": "oregon",
                "plan": "starter"
            }
        }


        # Log payload
        logging.info(f"Payload for Render API: {payload}")
        logging.info(f"Full Payload for Render API: {payload}")

        # Validate JSON structure
        try:
            import json
            json.dumps(payload)  # Ensure payload is valid JSON
        except Exception as e:
            logging.error(f"Invalid JSON structure: {str(e)}")
            raise HTTPException(status_code=500, detail="Invalid JSON structure")

        # Create web service
        response = requests.post(render_api_url, headers=headers, json=payload)
        logging.info(f"Render API Response: {response.status_code} - {response.text}")

        if response.status_code != 201:
            raise HTTPException(status_code=500, detail=f"Failed to create web service: {response.json().get('message')}")

        # Retrieve public link
        service_id = response.json().get("id")
        public_url = response.json().get("url")

        return {"message": "Deployment successful", "public_link": public_url}

    except Exception as e:
        logging.error(f"Error during deployment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/owners")
async def get_owners():
    """Fetch valid owner IDs from Render."""
    try:
        render_api_url = "https://api.render.com/v1/owners"
        headers = {
            "Authorization": f"Bearer {RENDER_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.get(render_api_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to fetch owner IDs: {response.json().get('message')}")

        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)