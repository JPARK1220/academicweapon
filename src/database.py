from contextlib import asynccontextmanager
import aioboto3
from supabase import create_async_client
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.config import settings
from src.conversations.schemas.conversation import Conversation
from src.conversations.schemas.message import Message
from src.conversations.schemas.settings import Settings
import redis.asyncio as redis

# Global variable
supabase = None
mongo_client = None
bucket = None
session = None

async def initialize_supabase():
    global supabase
    supabase = await create_async_client(
        supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
    )

async def connect_mongodb():
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[Conversation],  # List all Beanie Document models
    )

def disconnect_mongodb():
    global mongo_client
    if mongo_client is not None:
        mongo_client.close()

async def initialize_redis():
    global redis_client
    redis_client = redis.Redis(
        host = settings.REDIS_HOST,
        port = settings.REDIS_PORT,
        password = settings.REDIS_PASSWORD,
        decode_responses=True,
    )
    await redis_client.ping()

async def disconnect_redis():
    global redis_client
    if redis_client is not None:
        await redis_client.close()

async def initialize_bucket():
    global session, bucket
    
    # Create an async session
    session = aioboto3.Session(
        aws_access_key_id=settings.S3_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_SECRET_ACCESS_KEY,
        region_name="auto"
    )
    
    # Use the session to get a resource client
    async with session.resource(
        service_name="s3",
        endpoint_url=settings.S3_ENDPOINT_URL
    ) as s3:
        bucket = await s3.Bucket(settings.S3_BUCKET)

# Helper function to get bucket for use in other functions
@asynccontextmanager
async def get_bucket():
    global session
    
    if session is None:
        await initialize_bucket()
    
    async with session.resource(
        service_name="s3",
        endpoint_url=settings.S3_ENDPOINT_URL
    ) as s3:
        bucket = await s3.Bucket(settings.S3_BUCKET)
        yield bucket

def get_redis():
    return redis_client

def get_supabase():
    return supabase
