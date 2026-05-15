import requests
from Utils.constants import BRIDGE_DEFAULT_URL
from Utils.logger import logger

class BridgeClient:
    """Client for communicating with the Radpretation Localhost Bridge (FastAPI/Next.js)."""
    
    def __init__(self, base_url=BRIDGE_DEFAULT_URL):
        self.base_url = base_url.rstrip('/')

    def get_status(self):
        """Check if the bridge is alive."""
        url = f"{self.base_url}/status"
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            logger.info("Localhost bridge is active.")
            return True
        except requests.RequestException as e:
            logger.error(f"Localhost bridge is not reachable: {e}")
            return False

    def report_upload_progress(self, progress, status_message):
        """Send upload progress updates to the bridge for the OHIF UI to display."""
        url = f"{self.base_url}/upload/progress"
        payload = {
            "progress": progress,
            "status": status_message
        }
        try:
            requests.post(url, json=payload, timeout=2)
        except requests.RequestException:
            # We don't want to crash if we can't report progress
            pass
