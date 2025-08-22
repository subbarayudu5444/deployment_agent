from fastapi import APIRouter
from services.deployment_service import DeploymentService

router = APIRouter(prefix="/api", tags=["deployment"])

@router.post("/deploy")
async def deploy_repository(repo_url: str):
    """Deploy a GitHub repository locally for testing."""
    return await DeploymentService.deploy_repository(repo_url)

@router.get("/status/{repo_name}")
async def check_deployment_status(repo_name: str):
    """Check if both backend and frontend are running for a deployed repo."""
    return await DeploymentService.check_deployment_status(repo_name)