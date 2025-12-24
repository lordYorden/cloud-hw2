from datetime import datetime
from typing import Optional, Any, Dict
from beanie import Document
from pydantic import Field, EmailStr, BaseModel, Json
from zoneinfo import ZoneInfo
from enum import Enum
from beanie import Document, PydanticObjectId
from pydantic import model_validator, field_serializer
import json

ZONE = ZoneInfo('Asia/Jerusalem')

class MessageEntity(Document):
    message: str
    target: EmailStr
    sender: EmailStr
    title: str
    urgent: bool = Field(default=False)
    publicationTimestamp: datetime = Field(default_factory=lambda: datetime.now(ZONE))
    moreDetails: Dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def handle_invalid_id(cls, data: dict) -> dict:
        if isinstance(data, dict):
            for key in ["id", "_id"]:
                val = data.get(key)
                if isinstance(val, str) and len(val) != 24:
                    data.pop(key, None)
        
        return data
    
    class Settings:
        name = "messages" # The MongoDB collection name

class MessageBoudary(BaseModel):
    id: Optional[str]
    target: EmailStr
    sender: EmailStr
    title: str
    moreDetails: Dict[str, Any] = Field(default_factory=dict)
    urgent: bool
    message: str
    publicationTimestamp: datetime

    @classmethod
    def from_entity(cls, entity: MessageEntity):
        return cls(
            id=str(entity.id) if entity.id else None,
            message=entity.message,
            publicationTimestamp=entity.publicationTimestamp,
            target=entity.target,
            sender=entity.sender,
            title=entity.title,
            urgent=entity.urgent,
            moreDetails=entity.moreDetails
        )
    
    def to_entity(self) -> MessageEntity:
        data = self.model_dump()
        if 'id' in data:
            data['_id'] = PydanticObjectId(data.pop('id'))
        return MessageEntity(**data)
    
    @field_serializer('publicationTimestamp')
    def serialize_timestamp(self, value: datetime) -> str:
        if value:
            return value.astimezone(ZONE).isoformat(timespec='milliseconds')
        return None
class Criteria(Enum):
    RECIPIENT = "byRecipient"
    SENDER = "bySender"