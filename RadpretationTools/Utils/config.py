import qt

class ConfigManager:
    """Manages PACS configuration settings via Slicer's QSettings."""
    
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.settings = qt.QSettings()

    @property
    def pacs_url(self):
        return self.settings.value("Radpretation/PACS_URL", "http://localhost:8042")

    @pacs_url.setter
    def pacs_url(self, value):
        self.settings.setValue("Radpretation/PACS_URL", value)

    @property
    def dicomweb_path(self):
        return self.settings.value("Radpretation/DICOMWebPath", "/dicom-web")

    @dicomweb_path.setter
    def dicomweb_path(self, value):
        self.settings.setValue("Radpretation/DICOMWebPath", value)

    @property
    def auth_mode(self):
        return self.settings.value("Radpretation/AuthMode", "None")

    @auth_mode.setter
    def auth_mode(self, value):
        self.settings.setValue("Radpretation/AuthMode", value)

    @property
    def username(self):
        return self.settings.value("Radpretation/Username", "")

    @username.setter
    def username(self, value):
        self.settings.setValue("Radpretation/Username", value)

    @property
    def password(self):
        return self.settings.value("Radpretation/Password", "")

    @password.setter
    def password(self, value):
        self.settings.setValue("Radpretation/Password", value)

    # Helper properties
    @property
    def dicomweb_endpoint(self):
        pacs = self.pacs_url.rstrip('/')
        path = self.dicomweb_path
        if path and not path.startswith('/'):
            path = '/' + path
        return f"{pacs}{path}"

    @property
    def orthanc_wado_uri(self):
        pacs = self.pacs_url.rstrip('/')
        return f"{pacs}/wado"

    def get_requests_kwargs(self):
        """Returns kwargs to unpack into requests calls (e.g. auth)."""
        if self.auth_mode == "Basic Auth" and self.username:
            return {"auth": (self.username, self.password)}
        return {}

LOCAL_BRIDGE_PORT = 5000

config = ConfigManager.get_instance()
