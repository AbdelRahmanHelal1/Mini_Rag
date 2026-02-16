from .BaseController import BaseController
from fastapi import UploadFile  
from models import ResponseSignal
from models.db_schemes import ProjectDBScheme
from models.db_schemes import Data_Chunk
from typing import List
from stores.llm import LLMEnums,CohereEnums
import json
import os


class NLPController(BaseController):

    def __init__(self, vectordb_client,generation_client,embedding_client,Tempelete_parser):
        super().__init__()


        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client
        self.Tempelete_parser=Tempelete_parser

    def create_collection_name(self,prject_id:str):
        return f"collection_{prject_id}".strip()
    
    def reset_vectordb_collection(self,project:ProjectDBScheme):
        collection_name=self.create_collection_name(prject_id=project.id)

        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vectordb_collection_info(self,project:ProjectDBScheme):

        collection_name=self.create_collection_name(prject_id=project.id)
        collection_info= self.vectordb_client.get_collection_info(collection_name=collection_name)  
       
        return json.loads(json.dumps(collection_info, default=lambda x: x.__dict__))

    def index_into_vectordb(self,project:ProjectDBScheme,
                            chunks:List [Data_Chunk],
                            chunks_id: List[int] ,
                            do_reset: bool=False):
        
        # get collection name
        collection_name=self.create_collection_name(prject_id=project.id)

        # mange items
        texts=[chunk.chunk_text for chunk in chunks ]
        metadata=[chunk.chunk_metadata for chunk in chunks ]
        #orders=[chunk.chunk_order for chunk in chunks ]

        vectors=[
                self.embedding_client.embedding_text(
                    text=text,
                    document_type=CohereEnums.DOCUMENT.value )
                    for text in texts
        ]

        #create collection if not exist

        _=self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset)

        # insert data into collection

        _=self.vectordb_client.insert_many(
            collection_name= collection_name,
            text =texts,
            vector=vectors,
            metadata=metadata,
            record_id=chunks_id,
            )
        
        return True
    
    def search_in_vectordb(self,project:ProjectDBScheme,
                          text:str,
                          limit:int=3):

        collection_name=self.create_collection_name(prject_id=project.id)

        # get embedding for text

        vector=self.embedding_client.embedding_text(
                    text=text,
                    document_type=CohereEnums.QUERE.value )

        # search in vectordb

        results=self.vectordb_client.serch_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        return results
    
    def answer_rag_question(self,project:ProjectDBScheme,
                          query:str,
                          limit:int=3):
        
        answer,full_prompt,chat_history=None,None,None
        
        # get retrived releted collection

        retrived_doc =self.search_in_vectordb(
            project=project,        
            text=query,
            limit=limit)
        
        if not retrived_doc or len(retrived_doc)==0:
            return answer,full_prompt,chat_history
        
        # construct LLM prompt
        system_prompt= self.Tempelete_parser.get("rag","System_Prompt")
        

        documents_prompt="\n".join([
            self.Tempelete_parser.get("rag","Document_Prompt",{
                "doc_num":idx+1,
                "chunk_text":doc.text
            })

            for idx,doc in enumerate ( retrived_doc)
        ])

        Footer_Prompt= self.Tempelete_parser.get("rag","Footer_Prompt",{
            "query":query
        })


        chat_history=[
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enmus.SYSTEM.value
            )
        ]

        full_prompt="\n\n".join([documents_prompt,Footer_Prompt])

        answer=self.generation_client.generation_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer,full_prompt,chat_history


                                               


