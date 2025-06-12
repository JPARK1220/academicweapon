from src.database import get_postgres_session

async def get_db_session():
    async with get_postgres_session()() as session:
        yield session