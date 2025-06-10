from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker,async_scoped_session
from asyncio import current_task

from config import settings

class Database_helper:
    def __init__(self,url:str,echo:bool):
        self.engine = create_async_engine(url=url,echo=echo)

        self.session_factory = async_sessionmaker(
            autoflush=echo,
            expire_on_commit=echo,
            bind=self.engine,
            autocommit = echo


    )
    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return session


    async def get_session(self):
        async with self.session_factory() as session:
            yield session
            await session.close()


    async def get_smart_session(self):
        session = self.get_scoped_session()
        async with session() as scoped_session:
            yield scoped_session
            await scoped_session.close()


db_helper = Database_helper(url=settings.db_url,echo=settings.db_echo)