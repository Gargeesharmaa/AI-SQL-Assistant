import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from config.settings import settings

logger = logging.getLogger(__name__)

engine = create_async_engine(
    settings.async_databasse_url,
    echo=settings.DEBUG,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_readonly_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            await session.excute(text("SET TRANSACTION READ ONLY;"))
            yield session
        except Exception as e:
            logger.error(f"database session erorr: {str(e)}")
            await session.rollback()
            raise e
        finally:
            await session.close()

async def check_db_connection() -> bool:
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1;"))
            return result.scalar()==1
    except Exception as e:
        logger.error(f"Failed connection check to PostgresSQL: {e}")
        return False