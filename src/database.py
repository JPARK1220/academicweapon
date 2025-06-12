from contextlib import asynccontextmanager
import aioboto3
from supabase import create_async_client
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
import redis.asyncio as redis

# Global variable
supabase = None
postgres_engine = None
postgres_session = None
bucket = None
session = None

async def initialize_supabase():
    global supabase
    supabase = await create_async_client(
        supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
    )

async def initialize_postgres():
    global postgres_engine, postgres_session
    postgres_engine = create_async_engine(settings.POSTGRES_URL, echo=True)
    postgres_session = async_sessionmaker(postgres_engine, expire_on_commit=False)

async def disconnect_postgres():
    global postgres_engine
    if postgres_engine:
        await postgres_engine.dispose()

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

def get_postgres_session():
    return postgres_session


# Extra setup for SqlAlcehmy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

class Base(AsyncAttrs, DeclarativeBase):
    pass
