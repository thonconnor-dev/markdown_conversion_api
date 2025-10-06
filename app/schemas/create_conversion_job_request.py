
from pydantic import BaseModel

class CreateConversionJobRequest(BaseModel):
    original_filename: str