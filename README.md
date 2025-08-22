# Coastal Seven Deployment Agent

Automated deployment agent that deploys GitHub repositories locally with both frontend and backend support.

## Project Structure

```
AGENT-SDLC/
├── backend/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── deployment.py    # Deployment endpoints
│   │   └── lightning.py     # Lightning.ai integration
│   ├── deployments/         # Deployed repositories
│   ├── config.py           # Configuration and environment
│   ├── main.py             # FastAPI app entry point
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables
└── README.md
```

## Quick Start

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   # Create .env file with:
   LIGHTNING_API_KEY=your_lightning_api_key
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Access the API:**
   - API Documentation: http://127.0.0.1:8000/docs
   - Deploy endpoint: `POST /api/deploy`
   - Status endpoint: `GET /api/status/{repo_name}`

## API Endpoints

### Deployment
- `POST /api/deploy` - Deploy a GitHub repository
- `GET /api/status/{repo_name}` - Check deployment status

### Lightning.ai
- `GET /api/test-graphql` - Test Lightning.ai GraphQL connection

## Usage Example

```bash
# Deploy a repository
curl -X POST "http://127.0.0.1:8000/api/deploy" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/username/repository.git"}'

# Check status
curl "http://127.0.0.1:8000/api/status/repository"
```

## Features

- ✅ Automatic GitHub repository cloning
- ✅ Frontend and backend deployment
- ✅ Automatic port management
- ✅ API URL synchronization
- ✅ Health checks and status monitoring
- ✅ Lightning.ai integration ready