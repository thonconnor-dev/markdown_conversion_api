
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Text
from app.schemas.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID, TIMESTAMP
from uuid import UUID


class JobHistory(Base):
    __tablename__ = 'jobs_history'
    id : Mapped[UUID] = mapped_column(PGUUID(as_uuid=True),
                                      nullable=False,
                                      primary_key=True)
    job_id : Mapped[UUID] = mapped_column(PGUUID, 
                                          ForeignKey('conversion_jobs.id'), 
                                          nullable=False)
    status : Mapped[str] = mapped_column(Text, nullable=False)
    error_detail : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    markdown_path : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable= False)