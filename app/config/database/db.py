# app/config/database/db.py
import contextlib
from datetime import datetime
from typing import AsyncIterator
from sqlalchemy import func, event
from sqlalchemy.ext.asyncio import (
    AsyncConnection, 
    AsyncEngine, 
    AsyncSession,
    async_sessionmaker, 
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, String
from sqlalchemy.ext.declarative import declared_attr
from app.utils.uuid_generator import id_gen
class Base(DeclarativeBase):
    pass


class TimeStamp:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
    deleted_at: Mapped[datetime] = mapped_column(DateTime, unique=True, nullable=True)

class BaseModelClass(Base, TimeStamp):
    __abstract__ = True
    
    @declared_attr
    def id(cls) -> Mapped[str]:
        return mapped_column(
            String(255),
            primary_key=True,
            default=id_gen,
            unique=True
        )
    @classmethod
    def __declare_last__(cls):
        @event.listens_for(cls, 'before_insert')
        def receive_before_insert(mapper, connection, instance):
            if instance.id is None:
                instance.id = id_gen()    


class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(
            host,
            echo=False,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)

session_manager = DatabaseSessionManager()

async def get_db() -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session


# import contextlib
# from datetime import datetime
# from typing import AsyncIterator, Literal

# from fastapi import Depends
# from sqlalchemy import create_engine, func
# from sqlalchemy.engine import Engine
# from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
#                                     async_sessionmaker, create_async_engine)
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import (DeclarativeBase, Mapped, Session, declarative_base,
#                             mapped_column, relationship, sessionmaker)

# from app.config import env
# from app.utils.logger import log

# # SQLALCHEMY_DATABASE_URL: Literal["sqlite:///./flow.db"] = "sqlite:///./flow.db"

# # engine: Engine = create_engine(
# #     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# # )

# engine: Engine = create_engine(env.env['database_url'])
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base(

# class Base(DeclarativeBase):
#     pass

# class DatabaseSessionManager:
#     def __init__(self):
#         self._engine: AsyncEngine | None = None
#         self._sessionmaker: async_sessionmaker | None = None

#     def init(self, host: str):
#         self._engine = create_async_engine(
#             host,
#             echo=False,  # Set to True for SQL query logging
#             pool_pre_ping=True,  # Enable connection pool pre-ping
#             pool_size=10,  # Maximum number of connections in the pool
#             max_overflow=20  # Maximum number of connections that can be created beyond pool_size
#         )
#         self._sessionmaker = async_sessionmaker(
#             bind=self._engine,
#             expire_on_commit=False,
#             autoflush=False,
#             autocommit=False
#         )

#     async def close(self):
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")
#         await self._engine.dispose()
#         self._engine = None
#         self._sessionmaker = None

#     @contextlib.asynccontextmanager
#     async def connect(self) -> AsyncIterator[AsyncConnection]:
#         if self._engine is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._engine.begin() as connection:
#             try:
#                 yield connection
#             except Exception:
#                 await connection.rollback()
#                 raise
#             finally:
#                 await connection.close()

#     @contextlib.asynccontextmanager
#     async def session(self) -> AsyncIterator[AsyncSession]:
#         if self._sessionmaker is None:
#             raise Exception("DatabaseSessionManager is not initialized")

#         async with self._sessionmaker() as session:
#             try:
#                 yield session
#             except Exception:
#                 await session.rollback()
#                 raise
#             finally:
#                 await session.close()

#     # Used for testing
#     async def create_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.create_all)

#     async def drop_all(self, connection: AsyncConnection):
#         await connection.run_sync(Base.metadata.drop_all)


# session_manager = DatabaseSessionManager()
# async def get_db():
#     async with session_manager.session() as session:
#        yield session




# class TimeStamp(object):
#     created_at: Mapped[datetime] = mapped_column(default=func.now())
#     updated_at: Mapped[datetime] = mapped_column(default=func.now())
