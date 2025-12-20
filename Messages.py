from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import Field, BaseModel
from zoneinfo import ZoneInfo
from typing import Annotated
from beanie import Document, PydanticObjectId
from pydantic import Field, BeforeValidator

# class UserInfo(BaseModel):
#     """Embedded document (Like a Java Nested Object)"""
#     email: str
#     display_name: str

SafeId = Annotated[
    Optional[PydanticObjectId], 
    BeforeValidator(lambda v: None if isinstance(v, str) and len(v) != 24 else v)
]

ZONE = ZoneInfo('Asia/Jerusalem')

class Message(Document):
    id: SafeId = Field(default=None, alias="_id")
    message: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZONE))

    class Settings:
        name = "messages" # The MongoDB collection name