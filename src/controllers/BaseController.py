from helpers.config import get_settings, Settings
from fastapi import Depends
import os 
import random
import string
import re

class BaseController:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.settings = settings
        self.base_dire=os.path.dirname(os.path.dirname(__file__)) # Get the base directory of the project
        self.file_dire=os.path.join(self.base_dire, "assets", "files")
        self.database_dire=os.path.join(self.base_dire, "assets", "database")

    def get_clean_path(self, orig_name: str):
        """
        Cleans the given path by removing any leading or trailing slashes.
        """
        cleaned_name = re.sub(r'[^\w.]', ' ', orig_name.strip())
        cleaned_name=cleaned_name.replace(" ", "_")  # Replace spaces with underscores
        return cleaned_name
    
    def generate_random_string(self, length: int = 10):
        """
        Generates a random string of fixed length.
        """
    
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))
    
    def get_database_path(self,database_name: str):

        database_path=os.path.join(self.database_dire ,database_name)

        if os.path.exists(database_path):
            return database_path
        else:
            os.makedirs(database_path)
            return database_path


       