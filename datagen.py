from Messages import MessageEntity

async def seed_data():
    count = await MessageEntity.count()
    
    if count == 0:
        messages = [
            MessageEntity(
                message="Hello reactive world",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Greeting"
            ),
            MessageEntity(
                message="Streaming is efficient",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Architecture Update"
            ),
            MessageEntity(
                message="Python is fast too",
                target="receiver@example.com",
                sender="sender@example.com",
                title="Performance Review",
                urgent=True
            ),
        ]
        
        await MessageEntity.insert_many(messages)