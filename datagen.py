from Messages import MessageEntity

async def seed_data():
    count = await MessageEntity.count()
    
    if count == 0:
        messages = [
            MessageEntity(
                message="Hello reactive world",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Greeting",
                moreDetails={"info": "This is a test message"}
            ),
            MessageEntity(
                message="Streaming is efficient",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Architecture Update",
                moreDetails={"info": "Streaming over REST is efficient"}
            ),
            MessageEntity(
                message="Python is fast too",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Performance Review",
                urgent=True,
                moreDetails={"info": "Python with async can be fast"}
            ),
        ]
        
        await MessageEntity.insert_many(messages)