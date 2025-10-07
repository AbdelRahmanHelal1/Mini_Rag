from abc import ABC, abstractmethod

class VectorDBinterface(ABC):

    @abstractmethod
    def Connect(self):
        pass

    @abstractmethod
    def Disconnect(self):
        pass

    @abstractmethod
    def is_collection_exists(self ,collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> list:
        pass
    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str) :
        pass

    @abstractmethod
    def create_collection(self, collection_name: str,
                           embedding_size: int,
                           dorest: bool = False) :
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text :str ,vector: list,
                    metadata: dict = None,
                    record_id: str = None) :
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, text :list ,vector: list,
                    metadata: list = None,
                    record_id: list = None,
                    batch_size: int = 50) :
        pass

    @abstractmethod
    def serch_by_vector(self, collection_name: str,
                        vector :str ,limit :int):
        pass
    
