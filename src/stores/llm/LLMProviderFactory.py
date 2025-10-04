from .LLMEnums import LLMEnums
from .Provider import OpenAIProvider, CoHereProvider
class LLMProviderFactory:

    def __init__(self,config :dict):
 
        self.config=config


    def create(self,provider :str):

        if provider==LLMEnums.OPENAI.value:
            OpenAIProvider(
                api_key = self.config.OpenAI_API_KEY ,  
                df_input_max_char = self.config.DEFAULT_MAX_INPUT_CHARACTER,
                df_output_max_char = self.config.DEFAULT_MAX_OUTPUT_CHARACTER,
                df_temperature =self.config.GENERATION_DAFAULT_TEMPERATURE 

            )

        if provider==LLMEnums.COHERE.value:
            CoHereProvider(
                api_key = self.config.COHERE_API_KEY ,  
                df_input_max_char = self.config.DEFAULT_MAX_INPUT_CHARACTER,
                df_output_max_char = self.config.DEFAULT_MAX_OUTPUT_CHARACTER,
                df_temperature =self.config.GENERATION_DAFAULT_TEMPERATURE 

            )

        return None
