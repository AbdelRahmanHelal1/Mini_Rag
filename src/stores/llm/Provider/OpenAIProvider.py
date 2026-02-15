from ..LLMInterface import LLMInterface
from ..LLMEnums import LLMEnums,OpenAIEnums
from openai import OpenAI
import logging
class OpenAIProvider(LLMInterface):

    def __init__(self,api_key:str,df_input_max_char:int=1000,
                 
                 df_output_max_char:int=1000,df_temperature:float=0.1):
        
        self.api_key = api_key    
        self.df_input_max_char = df_input_max_char
        self.df_output_max_char = df_output_max_char
        self.df_temperature = df_temperature

        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None
        self.enmus=OpenAIEnums

        self.client=OpenAI(api_key=self.api_key)
        
        self.logger = logging.getLogger(__name__)

    def process_text(self,text:str):
        return text[:self.df_input_max_char].strip()

    def set_generation_model(self, model_id: str):
        self.generation_model_id=model_id

    def set_embedding_model(self, model_id: str,embedding_size:int=None):
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size

    def generation_text(self, prompt: str,chat_history:list=[],
                    max_out_tokecn:int=None ,
                        temperature :float=None):
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.generation_model_id :
            self.logger.error("Generation model is not set.")
            return None
        max_out_tokecn=max_out_tokecn if max_out_tokecn else self.df_output_max_char
        temperature=temperature if temperature else self.df_temperature 

        chat_history.append(self.construct_prompt(
            role=OpenAIEnums.USER.value,
            prompt=prompt
        ))

        response=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_out_tokecn,
            temperature=temperature
        )

        if not response or not response.choices or len(response.choices)==0 or not  response.choices[0].message :
            self.logger.error("No response data received from OpenAI.")
            return None
        
        return response.choices[0].message.content



        


    def embedding_text(self, text: str, document_type: str=None):
        
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.embedding_model_id :
            self.logger.error("Embedding model is not set.")
            return None
        response=self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text
        )

        if not response or not response.data or len(response.data)==0 or not  response.data[0].embedding :
            self.logger.error("No embedding data received from OpenAI.")
            return None
        
        return response.data[0].embedding

        
        

    def construct_prompt(self, prompt: str, role: str):
        return{
            "role":role,
            "content":self.process_text(prompt)
        }