from ..VectorDBinterface import VectorDBinterface
from ..VectorDBEnums import DistanceMethodEnums
from qdrant_client import QdrantClient ,models
import logging


class QdrantDB(VectorDBinterface):
    def __init__(self,db_path:str ,distance_method:str):

        self.db_path = db_path
        self.distance_method = None
        self.client = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.EUCLIDEAN.value:
            self.distance_method = models.Distance.EUCLIDEAN    
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def Connect(self):
        self.client=QdrantClient(path=self.db_path)

    def Disconnect(self):
        self.client=None

    def is_collection_exists(self ,collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> list:
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
       return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str) :
        if self.client.collection_exists(collection_name):
           return self.client.delete_collection(collection_name=collection_name)
    


    def create_collection(self, collection_name: str,
                           embedding_size: int,
                           dorest: bool = False) :
        
        if dorest :
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exists(collection_name=collection_name):

            _ = self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method)
                    )
            return True
        else:
            self.logger.warning(f"Collection {collection_name} already exists.")
            return False
        
    def insert_one(self, collection_name: str, text :str ,vector: list,
                    metadata: dict = None,
                    record_id: str = None) :
        
        if not self.is_collection_exists(collection_name=collection_name):
            self.logger.error(f"Collection {collection_name} does not exist.")
            return False
        
        try :
            _ = self.client.upload_records(

                    collection_name=collection_name,
                    records=[   
                        models.Record(
                            vector=vector,
                            payload={"text": text, "metadata":metadata }
                        )
                    ]
                )
        except Exception as e:
            self.logger.error(f"Error inserting record: {e}") 
            return False


        return True
    
    def insert_many(self, collection_name: str, text :list ,vector: list,
                    metadata: list = None,
                    record_id: list = None,
                    batch_size: int = 50) :
        
        if metadata is None:
            metadata = [None] * len(text)
        
        if record_id is None:
            record_id = [None] * len(text)

        for i in range(0, len(text), batch_size):
            batch_end= i + batch_size
            batch_text = text[i:batch_end]
            batch_vector = vector[i:batch_end]
            batch_metadata = metadata[i:batch_end]


            records = [
                models.Record(
                    vector=vec,
                    payload={"text": txt, "metadata": meta}
                )
                for txt, vec, meta in zip(batch_text, batch_vector, batch_metadata)
            ]

            try :

                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=records
                )
            except Exception as e:
                self.logger.error(f"Error inserting batch starting at index {i}: {e}")
                return False
        return True
    
    def serch_by_vector(self, collection_name: str,
                        vector :str ,limit :int):
        return sself.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

    

        