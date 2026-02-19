from helper.config import get_settings, Setting

class BaseDataModel:
     def __init__(self, db_client):
        self.db_client = db_client
        self.settings: Setting = get_settings()