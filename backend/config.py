import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Environment variables
LIGHTNING_API_KEY = os.getenv("LIGHTNING_API_KEY")

if not LIGHTNING_API_KEY:
    logging.warning("LIGHTNING_API_KEY not found in environment variables")

# App configuration
APP_CONFIG = {
    "title": "Coastal Seven Deployment Agent",
    "description": "Automated deployment agent for GitHub repositories",
    "version": "1.0.0"
}