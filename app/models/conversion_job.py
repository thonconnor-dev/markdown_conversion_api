
from datetime import datetime
from typing import Optional
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, TIMESTAMP

from sqlalchemy import (
    Text
)
from uuid import UUID


class ConversionJob(Base):
    __tablename__ = 'conversion_jobs'
    
    id : Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    original_filename : Mapped[str] = mapped_column(Text, nullable=False)
    storage_path : Mapped[str] = mapped_column(Text, nullable=False)
    status : Mapped[str] = mapped_column(Text, nullable=False)
    error_detail : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    markdown_path : Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable= False)
    updated_at : Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable= False)