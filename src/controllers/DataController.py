from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseStatus
from .ProjectController import ProjectController
import re
import os



class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
    
    def validate_uploaded_file(self,file: UploadFile):
        
        if file.content_type not in self.settings.FILE_ALLOWED_TYPE:
            return False, ResponseStatus.FILE_TYPE_NOT_ALLOWED.value
        
        if file.size > self.settings.FILE_MAX_SIZE:
            return False, ResponseStatus.FILE_SIZE_EXCEEDS.value
        return True, ResponseStatus.FILE_VALID.value

    def generate_unique_filename(self,filename: str, project_id: str):
        random_file_name = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        cleanfilename = self.get_clean_file_name(filename)
        new_file_path = os.path.join(project_path, f"{random_file_name}_{cleanfilename}")

        while os.path.exists(new_file_path):
            random_file_name = self.generate_random_string()
            new_file_path = os.path.join(project_path, f"{random_file_name}_{cleanfilename}")
        
        return new_file_path
                            
    def get_clean_file_name(self,filename:str):
        
        cleaned_file_name = re.sub(r'[^\w.]','', filename.strip())
        cleaned_file_name = cleaned_file_name.replace(' ','_')
        return cleaned_file_name
