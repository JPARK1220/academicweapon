from supabase import create_async_client
from src.config import settings
from mongoengine import connect, disconnect

# Global variable
supabase = None


async def initialize_supabase():
    global supabase
    supabase = await create_async_client(
        supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
    )


def connect_mongodb():
    connect(host=settings.MONGODB_URI)


def disconnect_mongodb():
    disconnect()


def get_supabase():
    return supabase
