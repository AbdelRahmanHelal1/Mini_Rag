from .Provider import QdrantDB
from .VectorDBEnums import VectorDBEnums
from ...controllers import BaseController



class VectorDBProviderFactory:

    def __init__(self, settings: dict):
        self.settings = settings
        self.base_controller = BaseController()


    def create (self,provider):

        db_path=self.base_controller.get_database_path(self.settings.VECTOR_DB_PATH)

        if provider == VectorDBEnums.QDRANT.value:
            return QdrantDB(db_path=db_path,
                            distance_method=self.settings.VECTOR_DB_DISTANCE_METRIC)
        else:
            raise ValueError(f"Unsupported vector database provider: {provider}")