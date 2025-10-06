from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ConversionJobResponse(BaseModel):
    id: UUID
    original_filename: str
    status: str
    error_detail: Optional[str]
    markdown_path: Optional[str]
    created_at: datetime
