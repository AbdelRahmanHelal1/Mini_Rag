from .BaseController import BaseController
from fastapi import UploadFile  
from models import ResponseSignal
import os

class ProjectController(BaseController):
    def __init__(self):  
        super().__init__()
    

    def get_project_directory(self, project_id: str):
        """
        Returns the directory path for a given project ID.
        """
        project_id =os.path.join(self.file_dire, project_id)


        if not os.path.exists(project_id):
            os.makedirs(project_id)
            
        return project_id 