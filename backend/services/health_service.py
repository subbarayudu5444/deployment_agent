import requests
import time
import logging

class HealthService:
    @staticmethod
    def check_backend_health(backend_url: str, timeout: int = 15) -> bool:
        """Check if backend is ready and responding."""
        for i in range(timeout):
            try:
                health_check = requests.get(backend_url, timeout=2)
                if health_check.status_code == 200:
                    logging.info(f"Backend ready at {backend_url}")
                    return True
            except:
                pass
            time.sleep(1)
        return False
    
    @staticmethod
    def check_frontend_health(frontend_url: str, timeout: int = 60) -> bool:
        """Check if frontend is ready and responding."""
        logging.info(f"Waiting for frontend to start at {frontend_url}...")
        
        for i in range(timeout):
            try:
                health_check = requests.get(frontend_url, timeout=2)
                if health_check.status_code == 200:
                    logging.info(f"Frontend ready at {frontend_url}")
                    return True
            except:
                if i % 15 == 0:
                    logging.info(f"Still waiting for frontend... ({i*2}s elapsed)")
            time.sleep(2)
        return False
    
    @staticmethod
    def check_service_status(url: str) -> str:
        """Check if a service is running, starting, or down."""
        try:
            response = requests.get(url, timeout=2)
            return "running" if response.status_code == 200 else "down"
        except:
            return "starting"