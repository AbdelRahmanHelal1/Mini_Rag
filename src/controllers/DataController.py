from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import  ProjectController
import os
class DataController(BaseController):
    def __init__(self, settings):  # ← استقبل الإعدادات هنا
        super().__init__()
        self.settings = settings   # ← خزن الإعدادات

    def validate_uploaded_file(self, file: UploadFile):
        allowed_extensions = self.settings.FILE_ALLOWED_EXTENSIONS
        max_size_mb = self.settings.FILE_MAX_SIZE  # ← استخرج الحجم الأقصى من الإعدادات

        print(ResponseSignal.FILE_TYPE, file.content_type)  # ← هنا نطبع نوع الملف

        if file.content_type not in allowed_extensions:
            return ResponseSignal.FILE_UPLOAD_NOT_ALLOWED.value # +f" : {allowed_extensions}"

        contents = file.file.read()
        size_in_bytes = len(contents)
        file.file.seek(0)

        if size_in_bytes > max_size_mb * 1024 * 1024:
            return ResponseSignal.FILE_UPLOAD_SIZE_EXCEEDED.value # +f" {max_size_mb} MB."

        return True , ResponseSignal.FILE_UPLOAD_SUCCESS.value
    

    def generate_Uniqe_file_path(self, project_id: str, file_name: str):
        """
        Generates a file path for the uploaded file.
        """
        random_file_name = self.generate_random_string()
        project_directory = ProjectController().get_project_directory(project_id)
        clean_file_name = self.get_clean_path(file_name)
        new_file_path= os.path.join(project_directory, random_file_name+"_"+clean_file_name)
    
        while os.path.exists(new_file_path):
            random_file_name = self.generate_random_string()
            new_file_path = os.path.join(project_directory, random_file_name + "_" + clean_file_name)

        return new_file_path ,random_file_name + "_" + clean_file_name