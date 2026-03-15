from helper.config import Setting, get_settings
import os
import random
import string
class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.file_dir = os.path.join(self.base_dir, "assets", "files")
        self.db_dir = os.path.join(self.base_dir, "assets", "vectoreDB")

    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    def get_db_path(self,db_name):
        db_path =  os.path.join(self.db_dir,db_name)

        if not os.path.exists(db_path):
            os.makedirs(db_path)
        else:
            return db_path
            
