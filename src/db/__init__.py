from motor import motor_asyncio


url = "mongodb://localhost:27017"
client = motor_asyncio.AsyncIOMotorClient(url)
db = client["notes"]
