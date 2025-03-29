from supabase import create_async_client
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.config import settings
from src.conversations.schemas.conversation import Conversation
from src.conversations.schemas.message import Message
from src.conversations.schemas.settings import Settings

# Global variable
supabase = None
mongo_client = None

async def initialize_supabase():
    global supabase
    supabase = await create_async_client(
        supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
    )


async def connect_mongodb():
    global mongo_client
    print(settings.MONGODB_URI)
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[Conversation],  # List all Beanie Document models
    )

async def disconnect_mongodb():
    global mongo_client
    mongo_client.close()


def get_supabase():
    return supabase
