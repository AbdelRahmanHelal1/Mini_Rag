from pydantic import BaseModel
from typing import List, Optional

class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100  # Default chunk size 
    overlap:Optional[int] = 20
    do_reset :Optional[int] = 0 