# Deployment Agent

This project is a Deployment Agent that automates the deployment of GitHub repositories to Render.

## Workflow
1. User provides a GitHub public repository link.
2. The agent creates a new web service on Render:
   - Language: Python 3
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port 13000`
   - Plan: Free
3. The agent retrieves the public Render link and returns it to the user.

## Environment Variables
- `RENDER_API_KEY`: API key for Render authentication.

## How to Run
1. Set the `RENDER_API_KEY` environment variable.
2. Start the backend server:
   ```bash
   python main.py
   ```
3. Send a POST request to `/deploy` with the GitHub repository URL.

## Example
```bash
curl -X POST http://127.0.0.1:8000/deploy -H "Content-Type: application/json" -d '{"repo_url": "https://github.com/username/repository.git"}'
```
