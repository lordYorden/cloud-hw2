from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager
from Messages import MessageBoudary, MessageEntity, Criteria
from beanie import init_beanie
from datetime import datetime
import logging
from Flux import to_flux
from fastapi import Depends
from fastapi_pagination import add_pagination, set_page
from pagination import ZeroBasedPage, ZeroBasedParams
from utils import sse_stream
from testcontainers.compose import DockerCompose
from datagen import seed_data
import re

client = None
compose = DockerCompose(".", compose_file_name="compose.yml")
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting up mongo")
    
    compose.start()
    
    host = compose.get_service_host("mongodb", 27017)
    port = compose.get_service_port("mongodb", 27017)
    
    db_url = f"mongodb://{host}:{port}"
    # startup
    await init_db(db_url)
    
    logger.info("DB initialized")
    
    yield
    # Clean up 
    compose.stop()
    logger.debug("Mongo stopped")

app = FastAPI(lifespan=lifespan)
set_page(ZeroBasedPage)
add_pagination(app)

async def init_db(db_url: str):
    global client
    
    client = AsyncMongoClient(db_url)

    # This line triggers the creation of the Unique Indexes defined in Annotated
    await init_beanie(database=client.chat_db, document_models=[MessageEntity])
    await seed_data()
    logger.debug("Database seeded successfully.")


@app.post("/message", response_model=MessageBoudary)
async def create_message(message: MessageBoudary):
    
    message.publicationTimestamp = datetime.now()
    message.id = None

    entity = message.to_entity()
    rv = await MessageEntity.insert_one(entity)
    return MessageBoudary.from_entity(rv)

@app.get("/messages")
@sse_stream(model=MessageBoudary)
async def get_messages(
    criteria: Criteria | None = None, 
    value: str | None = None,
    params: ZeroBasedParams = Depends()):

    cursor = MessageEntity.find({})

    messageFlux = (
        to_flux(cursor)
        .paginate(params)
        .map(lambda m: MessageBoudary.from_entity(m))
    )

    if criteria == Criteria.RECIPIENT and value:
        messageFlux = messageFlux.filter(lambda m: m.target == value)
    elif criteria == Criteria.SENDER and value:
        messageFlux = messageFlux.filter(lambda m: m.sender == value)

    return messageFlux

@app.delete("/messages", status_code=204)
async def delete_all_messages():
    await MessageEntity.delete_many({})

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="localhost", port=8080, log_level="debug")