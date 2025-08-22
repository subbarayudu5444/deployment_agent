import subprocess
import threading
import os
import logging

def start_backend_process(local_dir: str, backend_port: int):
    """Start backend process in a separate thread."""
    def start_backend():
        try:
            subprocess.run(
                ["uvicorn", "main:app", "--reload", "--host", "127.0.0.1", "--port", str(backend_port)],
                cwd=f"{local_dir}/backend",
                check=True
            )
        except Exception as e:
            logging.error(f"Failed to start backend: {str(e)}")
    
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    return backend_thread

def start_frontend_process(local_dir: str, frontend_port: int):
    """Start frontend process in a separate thread."""
    def start_frontend():
        try:
            logging.info(f"Installing frontend dependencies...")
            npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
            
            install_result = subprocess.run(
                [npm_cmd, "install"], 
                cwd=f"{local_dir}/frontend", 
                capture_output=True, 
                text=True,
                shell=True
            )
            if install_result.returncode != 0:
                logging.error(f"npm install failed: {install_result.stderr}")
                return
            
            logging.info(f"Starting frontend on port {frontend_port}...")
            env = os.environ.copy()
            env["PORT"] = str(frontend_port)
            start_result = subprocess.run(
                [npm_cmd, "start"], 
                cwd=f"{local_dir}/frontend", 
                env=env, 
                capture_output=True, 
                text=True,
                shell=True
            )
            if start_result.returncode != 0:
                logging.error(f"npm start failed: {start_result.stderr}")
        except Exception as e:
            logging.error(f"Failed to start frontend: {str(e)}")
    
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    return frontend_thread