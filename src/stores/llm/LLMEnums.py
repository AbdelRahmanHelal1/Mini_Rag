from enum import Enum


class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(Enum):
    
    SYSTEM = "developer" 
    USER   ="user"
    ASSISTANT="assistant"

class CohereEnums(Enum): 

    SYSTEM = "system"
    USER   = "user"
    ASSISTANT = "assistant"

    DOCUMENT="search_document"
    QUERE   ="search_query"

class DocumentTypeEnums(Enum):

    DOCUMENT="document"
    QUERE   ="query"

