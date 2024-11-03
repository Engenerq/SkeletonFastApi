from fastapi import FastAPI
from contextlib import asynccontextmanager

from asyncpg import create_pool

from app.core.config import get_settings
from app.core.db.codecs import init_codec


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.config = get_settings()
    app.state.pool = await create_pool(
        **app.state.config.db.dict(),
        init=init_codec,
    )
    yield
    app.state.pool.close()