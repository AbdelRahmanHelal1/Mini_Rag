from .BaseDataModel import BaseDataModel
from .db_schemes import ProjectDBScheme
from .enums.DataBaseEnums import DataBaseEnum
from .db_schemes import ProjectDBScheme

class ProjectModel(BaseDataModel):
    def __init__(self,db_client : object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_PROJECT_NAME.value]


    async def create_project(self,project : ProjectDBScheme) :
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id

        return project
    
    async def get_or_create_one(self,project_id : str ) :

        record = await self.collection.find_one(
            {"project_id": project_id}
        )

        if record is None :
            project = ProjectDBScheme(project_id=project_id)
            project =  await self.create_project(project=project)

            return project
        
        return ProjectDBScheme(**record)
    
    async def get_all_projects(self,page : int = 1, page_size : int = 10) :

        total_pages = await self.collection.count_documents({})
        total_pages = total_pages / page_size
        total_pages = int(total_pages) + (total_pages % 1 > 0)  

        cursor =self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(ProjectDBScheme(**document))

        return projects, total_pages
    
      


        