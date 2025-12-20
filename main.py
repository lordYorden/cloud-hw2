from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pymongo import AsyncMongoClient
from contextlib import asynccontextmanager
from Messages import Message
from beanie import init_beanie
from datetime import datetime
import logging
from Flux import to_flux
from fastapi import Depends
from fastapi_pagination import add_pagination, set_page
from pagination import ZeroBasedPage, ZeroBasedParams
from utils import sse_stream
from testcontainers.compose import DockerCompose

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

app = FastAPI(lifespan=lifespan)
set_page(ZeroBasedPage)
add_pagination(app)

async def init_db(db_url: str):
    global client
    
    client = AsyncMongoClient(db_url)

    # This line triggers the creation of the Unique Indexes defined in Annotated
    await init_beanie(database=client.chat_db, document_models=[Message])
    await seed_data()

async def seed_data():
    count = await Message.count()
    
    if count == 0:
        messages = [
            Message(message="Hello reactive world"),
            Message(message="Streaming is efficient"),
            Message(message="Python is fast too"),
        ]
        
        await Message.insert_many(messages)
        logger.debug("Database seeded successfully.")

@app.post("/message")
async def create_message(message: Message):
    
    message.created_at = datetime.now()
    message.id = None
    
    return await Message.insert_one(message)

@app.get("/messages")
@sse_stream
async def get_messages(params: ZeroBasedParams = Depends()):
    cursor = Message.find({})
    return (
        to_flux(cursor)
        .paginate(params)
        # .filter(lambda m: "hi" in m.message.lower())
        .map(lambda m: m.model_dump_json())
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080, log_level="debug")