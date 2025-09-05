from .BaseController import BaseController
from .ProjectController import  ProjectController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TXTLoader

import os
class ProcessController(BaseController):
    def __init__(self, file_id:str):  # ← استقبل الإعدادات هنا
        super().__init__()
        self.file_id = file_id  
        self.project_path= ProjectController().get_project_directory_by_file_id(file_id)


    def get_extension(self):
        return os.path.splitext(self.file_id)[-1]
    
    
    def load_document(self,file_id:str ,file_path:str):
        extension = self.get_extension()
        if extension == ".pdf":
            loader = PyMuPDFLoader(file_path)
        elif extension == ".txt":
            loader = TXTLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        documents = loader.load()
        return documents