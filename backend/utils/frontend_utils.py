import os
import re
import logging

def update_frontend_api_url(local_dir: str, backend_port: int) -> bool:
    """Update frontend API URL to use the correct backend port."""
    api_file_path = f"{local_dir}/frontend/src/services/api.js"
    
    if not os.path.exists(api_file_path):
        return False
    
    try:
        with open(api_file_path, 'r') as f:
            content = f.read()
        
        updated_content = re.sub(
            r"http://localhost:\d+", 
            f"http://localhost:{backend_port}", 
            content
        )
        
        with open(api_file_path, 'w') as f:
            f.write(updated_content)
        
        logging.info(f"Updated frontend API URL to use port {backend_port}")
        return True
    except Exception as e:
        logging.error(f"Failed to update frontend API URL: {str(e)}")
        return False

def has_frontend(local_dir: str) -> bool:
    """Check if the repository has a frontend."""
    return os.path.exists(f"{local_dir}/frontend/package.json")

def has_backend(local_dir: str) -> bool:
    """Check if the repository has a backend."""
    return os.path.exists(f"{local_dir}/backend/smain.py")