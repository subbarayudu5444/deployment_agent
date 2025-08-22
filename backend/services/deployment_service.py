import random
import logging
from fastapi import HTTPException
from utils.git_utils import clone_repository, extract_repo_name
from utils.frontend_utils import has_frontend, has_backend, update_frontend_api_url
from utils.process_utils import start_backend_process, start_frontend_process
from services.health_service import HealthService

# Store deployment info globally
active_deployments = {}

class DeploymentService:
    @staticmethod
    async def deploy_repository(repo_url: str):
        """Deploy a GitHub repository locally for testing."""
        try:
            # Validate GitHub repository URL
            if not repo_url.startswith("https://github.com/"):
                raise HTTPException(status_code=400, detail="Invalid GitHub repository URL")

            # Extract repository name and generate ports
            repo_name = extract_repo_name(repo_url)
            backend_port = random.randint(8001, 8999)
            frontend_port = random.randint(3001, 3999)
            local_dir = f"./deployments/{repo_name}"
            
            # Clone repository
            clone_repository(repo_url, local_dir)
            
            # Check what exists in the repository
            backend_exists = has_backend(local_dir)
            frontend_exists = has_frontend(local_dir)
            
            # Validate that at least one component exists
            if not backend_exists and not frontend_exists:
                return {
                    "message": "Deployment failed",
                    "error": "No backend or frontend found in repository",
                    "repo_name": repo_name
                }
            
            # Initialize variables
            backend_ready = False
            frontend_ready = False
            backend_url = None
            frontend_url = None
            
            # Deploy backend if exists
            if backend_exists:
                backend_url = f"http://127.0.0.1:{backend_port}"
                start_backend_process(local_dir, backend_port)
                backend_ready = HealthService.check_backend_health(backend_url)
                
                if not backend_ready:
                    return {
                        "message": "Backend deployment failed",
                        "error": "Backend failed to start",
                        "repo_name": repo_name
                    }
            
            # Deploy frontend if exists
            if frontend_exists:
                # Update API URL only if backend exists
                if backend_exists:
                    update_frontend_api_url(local_dir, backend_port)
                
                frontend_url = f"http://127.0.0.1:{frontend_port}"
                start_frontend_process(local_dir, frontend_port)
                frontend_ready = HealthService.check_frontend_health(frontend_url)
            
            # Store deployment info
            active_deployments[repo_name] = {
                "backend_port": backend_port if backend_exists else None,
                "frontend_port": frontend_port if frontend_exists else None
            }
            
            # Build response based on what was deployed
            result = {
                "message": "Deployment successful",
                "repo_name": repo_name,
                "local_path": local_dir,
                "status": "running"
            }
            
            # Add backend info if exists
            if backend_exists:
                result["backend_url"] = backend_url
                result["backend_port"] = backend_port
                result["docs_url"] = f"{backend_url}/docs"
            
            # Add frontend info if exists
            if frontend_exists:
                result["frontend_url"] = frontend_url
                result["frontend_port"] = frontend_port
            
            # Set appropriate note with missing component warnings
            if backend_exists and frontend_exists:
                if frontend_ready:
                    result["note"] = "Both frontend and backend are running"
                else:
                    result["note"] = "Backend running, frontend starting (may take 1-2 minutes)"
                    result["frontend_status"] = "starting"
            elif backend_exists:
                result["note"] = "Only backend is running"
                result["warning"] = "Frontend not found in repository"
            elif frontend_exists:
                if frontend_ready:
                    result["note"] = "Only frontend is running"
                else:
                    result["note"] = "Frontend starting (may take 1-2 minutes)"
                    result["frontend_status"] = "starting"
                result["warning"] = "Backend not found in repository"
                
            return result

        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Error during local deployment: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    @staticmethod
    async def check_deployment_status(repo_name: str):
        """Check if both backend and frontend are running for a deployed repo."""
        try:
            local_dir = f"./deployments/{repo_name}"
            if not os.path.exists(local_dir):
                return {"error": "Deployment not found"}
            
            backend_exists = has_backend(local_dir)
            frontend_exists = has_frontend(local_dir)
            
            result = {
                "repo_name": repo_name,
                "has_backend": backend_exists,
                "has_frontend": frontend_exists
            }
            
            if repo_name in active_deployments:
                backend_port = active_deployments[repo_name].get('backend_port')
                frontend_port = active_deployments[repo_name].get('frontend_port')
                
                if backend_port:
                    backend_url = f"http://127.0.0.1:{backend_port}"
                    result["backend_status"] = HealthService.check_service_status(backend_url)
                    result["backend_url"] = backend_url
                
                if frontend_exists and frontend_port:
                    frontend_url = f"http://127.0.0.1:{frontend_port}"
                    result["frontend_status"] = HealthService.check_service_status(frontend_url)
                    result["frontend_url"] = frontend_url
            else:
                result["backend_status"] = "unknown"
                if frontend_exists:
                    result["frontend_status"] = "unknown"
            
            return result
        except Exception as e:
            return {"error": str(e)}