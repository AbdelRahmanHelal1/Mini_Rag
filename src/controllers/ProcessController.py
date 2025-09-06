from .BaseController import BaseController
from .ProjectController import  ProjectController
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import ProcessingEnums
import os
class ProcessController(BaseController):
    def __init__(self,prject_id :str,file_id:str):  # ← استقبل الإعدادات هنا
        super().__init__()
        self.prject_id=prject_id
        self.file_id = file_id  
        self.project_path= ProjectController().get_project_directory(self.prject_id)


    def get_extension(self):
        return os.path.splitext(self.file_id)[-1]
    
    
    def load_document(self,file_id:str ):
        extension = self.get_extension()

        file_path = os.path.join(self.project_path, file_id)
        print(file_path, "**"*50)
        if extension == ProcessingEnums.Pdf.value:
            return PyMuPDFLoader(file_path)
        elif extension == ProcessingEnums.Txt.value:
            return TextLoader(file_path,encoding="utf-8")
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
    def get_file_content(self):
        loader = self.load_document(self.file_id)
        return loader.load()
    
    def Process_file_content(self, content:list, file_id:str,chunk_size:int =100, overlap:int =20):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
        )

        file_content_text=[
            rec.page_content
            for rec in content
        ]

        file_content_metadate=[
            rec.metadata
            for rec in content
        ]

        chunks=text_splitter.create_documents(file_content_text,
                                              metadatas= file_content_metadate)     


        return chunks