from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import ProjectDBScheme
from bson import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self,db_client : object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_ASSETS_NAME.value]

    
    @classmethod
    async def create_instance(cls,db_client: object):
        instance=cls(db_client=db_client)

        await instance.init_colledction()
        return instance

    async def init_colledction(self):
        all_collectons = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTIONS_ASSETS_NAME.value not in all_collectons :
            self.collection=self.db_client[DataBaseEnum.COLLECTIONS_ASSETS_NAME.value]
            indexs=Asset.get_index()
            for index in indexs :
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self,asset :Asset):
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id

        return asset
    
    async def get_all_project_assets(self,asset_project_id :str,asset_type:str):
        record= await self.collection.find({
            
        "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id,
        "asset_type" :asset_type }).to_list(length=None)

        return [Asset(**item) for item in record]
    
    async def get_asset_record(self,asset_project_id :str,asset_name:str):

        record= await self.collection.find_one({
            
        "asset_project_id":ObjectId(asset_project_id) if isinstance(asset_project_id,str) else asset_project_id,
        "asset_name" :asset_name })

        if record :
            return Asset(**record)
        else :  
            return None
        