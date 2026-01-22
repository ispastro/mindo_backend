from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=1000)

class ItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    location: str | None = Field(None, max_length=1000)

class ItemResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    location: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
