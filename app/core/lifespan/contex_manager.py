from fastapi import FastAPI
from contextlib import asynccontextmanager

from asyncpg import create_pool

from app.core.config import get_settings


@asynccontextmanager
def lifespan(app: FastAPI):
    app.state.config = get_settings()
    app.state.pool = create_pool(**app.state.config.db.dict())
    yield
    app.state.pool.close()
