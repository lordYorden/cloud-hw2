from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field, BaseModel
from zoneinfo import ZoneInfo
from typing import Annotated
from beanie import Document, PydanticObjectId
from pydantic import Field, BaseModel, model_validator, field_serializer, model_serializer

ZONE = ZoneInfo('Asia/Jerusalem')

class MessageEntity(Document):
    message: str
    publicationTimestamp: datetime = Field(default_factory=lambda: datetime.now(ZONE))

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
    message: str
    publicationTimestamp: datetime = Field(default_factory=lambda: datetime.now(ZONE))

    @classmethod
    def from_entity(cls, entity: MessageEntity):
        return cls(
            id=str(entity.id) if entity.id else None,
            message=entity.message,
            publicationTimestamp=entity.publicationTimestamp
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