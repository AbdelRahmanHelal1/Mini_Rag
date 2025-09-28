from .BaseDataModel import BaseDataModel
from .db_schemes import Data_Chunk
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import ProjectDBScheme
from pymongo import InsertOne 
from bson import ObjectId

class ChunkModel(BaseDataModel):
    def __init__(self,db_client : object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_CHUNKS_NAME.value]

    @classmethod
    async def create_instance(cls,db_client: object):
        instance=cls(db_client=db_client)

        await instance.init_colledction()
        return instance

    async def init_colledction(self):
        all_collectons = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTIONS_CHUNKS_NAME.value not in all_collectons :
            self.collection=self.db_client[DataBaseEnum.COLLECTIONS_CHUNKS_NAME.value]
            indexs=Data_Chunk.get_index()
            for index in indexs :
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )






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
        

        
    