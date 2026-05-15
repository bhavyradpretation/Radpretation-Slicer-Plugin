import requests
import json
from Utils.config import config
from Utils.logger import logger
from Models.StudyModel import StudyModel


class DICOMWebService:
    """Handles QIDO-RS and WADO-RS communication with Orthanc DICOMweb."""

    @staticmethod
    def _get_dicom_value(dicom_json, tag, default=""):
        try:
            if tag in dicom_json and "Value" in dicom_json[tag]:
                val = dicom_json[tag]["Value"]
                if len(val) > 0:
                    if isinstance(val[0], dict) and "Alphabetic" in val[0]:
                        return val[0]["Alphabetic"]
                    return str(val[0])
        except Exception:
            pass
        return default

    @staticmethod
    def fetch_study(study_uid):
        """Fetch a specific study from the DICOMweb endpoint (QIDO-RS), respecting pagination limits."""
        url = f"{config.dicomweb_endpoint}/studies?StudyInstanceUID={study_uid}&limit=1&includefield=StudyDate&includefield=PatientName&includefield=ModalitiesInStudy"
        try:
            logger.info(f"Fetching specific study from {url}")
            response = requests.get(url, timeout=5, **config.get_requests_kwargs())
            response.raise_for_status()
            studies_json = response.json()
            
            if not studies_json:
                return None
                
            s = studies_json[0]
            study = StudyModel(
                patient_name=DICOMWebService._get_dicom_value(s, "00100010", "Unknown"),
                patient_id=DICOMWebService._get_dicom_value(s, "00100020", "Unknown"),
                study_date=DICOMWebService._get_dicom_value(s, "00080020", ""),
                study_description=DICOMWebService._get_dicom_value(s, "00081030", ""),
                accession_number=DICOMWebService._get_dicom_value(s, "00080050", ""),
                study_instance_uid=DICOMWebService._get_dicom_value(s, "0020000D", study_uid),
                modalities=DICOMWebService._get_dicom_value(s, "00080061", "")
            )
            if not study.modalities:
                study.modalities = DICOMWebService._get_dicom_value(s, "00080061", "UNK")
                
            return study
        except Exception as e:
            logger.error(f"Failed to fetch DICOMweb study {study_uid}: {e}")
            return None

    @staticmethod
    def fetch_all_study_instances(study_uid):
        """Fetch list of all instances for a study in a single QIDO-RS request."""
        url = f"{config.dicomweb_endpoint}/studies/{study_uid}/instances"
        try:
            response = requests.get(url, timeout=10, **config.get_requests_kwargs())
            response.raise_for_status()
            instances_json = response.json()
            
            instance_map = []
            for i in instances_json:
                inst_uid = DICOMWebService._get_dicom_value(i, "00080018", "")
                series_uid = DICOMWebService._get_dicom_value(i, "0020000E", "")
                if inst_uid and series_uid:
                    instance_map.append((series_uid, inst_uid))
            return instance_map
        except Exception as e:
            logger.error(f"Failed to fetch all instances for study {study_uid}: {e}")
            return []

    @staticmethod
    def download_instance(study_uid, series_uid, instance_uid, output_path):
        """Download a single DICOM instance (WADO-URI)."""
        url = f"{config.orthanc_wado_uri}?requestType=WADO&studyUID={study_uid}&seriesUID={series_uid}&objectUID={instance_uid}&contentType=application/dicom"
        try:
            with requests.get(url, stream=True, timeout=10, **config.get_requests_kwargs()) as r:
                r.raise_for_status()
                with open(output_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True
        except Exception as e:
            logger.error(f"Failed to download instance {instance_uid}: {e}")
            return False
