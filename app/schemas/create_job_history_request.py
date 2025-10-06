import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class CreateJobHistoryRequest(BaseModel):
    job_id: UUID
    status: str
    error_detail: Optional[str]
    created_at: datetime