import requests
import json
import os
from Utils.config import config
from Utils.logger import logger

class OrthancClient:
    """Client for communicating with Orthanc PACS via its REST API."""
    
    def __init__(self, base_url=None):
        self.base_url = (base_url or config.pacs_url).rstrip('/')
        self.req_kwargs = config.get_requests_kwargs()

    def fetch_studies(self):
        """Fetch all studies from Orthanc."""
        url = f"{self.base_url}/studies?expand"
        try:
            response = requests.get(url, **self.req_kwargs)
            response.raise_for_status()
            logger.info("Successfully fetched studies from Orthanc.")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch studies from Orthanc: {e}")
            return []

    def lookup_study_id(self, study_instance_uid):
        """Find the Orthanc internal ID for a DICOM StudyInstanceUID."""
        url = f"{self.base_url}/tools/lookup"
        try:
            response = requests.post(url, data=study_instance_uid, **self.req_kwargs)
            response.raise_for_status()
            results = response.json()
            for res in results:
                if res.get("Type") == "Study":
                    return res.get("ID")
            return None
        except Exception as e:
            logger.error(f"Failed to lookup study ID for {study_instance_uid}: {e}")
            return None

    def download_study_archive(self, study_id, target_dir):
        """Download a study archive (ZIP) and extract it to the target directory."""
        url = f"{self.base_url}/studies/{study_id}/archive"
        import uuid
        zip_path = os.path.join(target_dir, f"{study_id}_{uuid.uuid4().hex}.zip")
        try:
            logger.info(f"Downloading study {study_id} from Orthanc...")
            with requests.get(url, stream=True, timeout=600, **self.req_kwargs) as r:
                r.raise_for_status()
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            logger.info(f"Successfully downloaded study to {zip_path}")
            return zip_path
        except Exception as e:
            logger.error(f"Failed to download study archive: {e}")
            return None

    def upload_dicom(self, file_path):
        """Upload a single DICOM file (e.g., DICOM SEG or RTStruct) to Orthanc."""
        url = f"{self.base_url}/instances"
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            headers = {'Content-Type': 'application/dicom'}
            response = requests.post(url, data=data, headers=headers, **self.req_kwargs)
            response.raise_for_status()
            logger.info(f"Successfully uploaded {file_path} to Orthanc.")
            return True
        except Exception as e:
            logger.error(f"Failed to upload DICOM to Orthanc: {e}")
            return False
