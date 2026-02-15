from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums,DocumentTypeEnums
import cohere
import logging


class CoHereProvider(LLMInterface):

    def __init__(self, api_key: str, df_input_max_char: int = 1000,
                 df_output_max_char: int = 1000, df_temperature: float = 0.1):

        self.api_key = api_key
        self.df_input_max_char = df_input_max_char
        self.df_output_max_char = df_output_max_char
        self.df_temperature = df_temperature
        self.enmus=CohereEnums

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        # ClientV2 (النسخة الجديدة)
        self.client = cohere.ClientV2(api_key=self.api_key)

        self.logger = logging.getLogger(__name__)

    def process_text(self, text: str):
        return text[:self.df_input_max_char].strip()

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int = None):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def generation_text(self, prompt: str, chat_history: list = None,
                        max_out_tokecn: int = None,
                        temperature: float = None):

        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model is not set.")
            return None

        max_out_tokecn = max_out_tokecn if max_out_tokecn else self.df_output_max_char
        temperature = temperature if temperature else self.df_temperature

        # لو chat_history مش متحدد
        if chat_history is None:
            chat_history = []

        chat_history.append(self.construct_prompt(
            role=CohereEnums.USER.value,
            prompt=prompt
        ))

        try:
            response = self.client.chat(
                model=self.generation_model_id,
                messages=chat_history,
                max_tokens=max_out_tokecn,
                temperature=temperature
            )
        except Exception as e:
            self.logger.error(f"Cohere chat request failed: {e}")
            return None

        # Cohere بيرجع response.message.content (list of Content objects)
        if not response or not response.message or not response.message.content:
            self.logger.error("No response data received from Cohere.")
            return None

        # ناخد أول قطعة نص
        return response.message.content[0].text

    def embedding_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model is not set.")
            return None
        
        input_type=CohereEnums.DOCUMENT.value
        if document_type ==DocumentTypeEnums.QUERE.value :
            CohereEnums.QUERE.value
            

        try:
            response = self.client.embed(
                model=self.embedding_model_id,
                texts=[self.process_text(text)],
                input_type=input_type,
                embedding_types=["float"],
            )
        except Exception as e:
            self.logger.error(f"Cohere embedding request failed: {e}")
            return None

        if not response or not response.embeddings or not response.embeddings.float :
            self.logger.error("No embedding data received from Cohere.")
            return None

        return response.embeddings.float[0]

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }
