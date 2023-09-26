# db_config.py
import configparser
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import urllib.parse

logger = logging.getLogger('motor')
logger.setLevel(logging.DEBUG)


config = configparser.ConfigParser()
config.read("config/config.ini")
mongodb_string = str(config.get("database", "mongodb_string"))
databasename = str(config.get("database", "databasename"))


#The database connection context manager
#(also where it actually connects to the database)

class Database:
    client = None
    db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(mongodb_string)
        self.db = self.client[databasename]

    async def close(self):
        self.client.close()

database = Database()

class DatabaseContextManager:
    async def __aenter__(self):
        await database.connect()
        return database.db

    async def __aexit__(self, exc_type, exc, tb):
        await database.close()

db_context = DatabaseContextManager()
