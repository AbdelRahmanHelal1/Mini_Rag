from .BaseDataModel import BaseDataModel
from .db_schemes import Data_Chunk
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import ProjectDBScheme
from pymongo import InsertOne 
from bson import ObjectId

class ChunkModel(BaseDataModel):
    def __init__(self,db_client : object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_PROJECT_NAME.value]

    async def create_data_chunk(self,chunk : Data_Chunk) :
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk
    
    async def get_chunk(self,chunk_id : str ) :

        record = await self.collection.find_one(
            {"_id": chunk_id}
        )

        if record is None :
            return None
        
        return Data_Chunk(**record)
    
    async def insert_many_chunks(self,chunks : list , batch_size : int = 100) :
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict(by_alias=True, exclude_unset=True)) for chunk in batch]

            if operations:
                await self.collection.bulk_write(operations) 


        return len(chunks)
    

    async def delete_chunks_by_project_id(self,project_id : ObjectId) :
        result = await self.collection.delete_many(
            {"chunk_project_id": project_id}
        )

        return result.deleted_count 
        

        
    