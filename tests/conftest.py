import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from tests.rollback_pool import RollBackAsyncPGPool

pytest_plugins = ["tests.fixtures"]


@pytest.fixture
def app() -> FastAPI:
    from app.main import Application
    return Application()()


@pytest.fixture
async def rollback_pool(app: FastAPI):
    pool = RollBackAsyncPGPool
    async with LifespanManager(app):
        app.state.pool = await pool.create_pool(app.state.pool)
        yield app


@pytest.fixture
def pool(rollback_pool: FastAPI):
    return rollback_pool.state.pool


@pytest.fixture
async def client(rollback_pool: FastAPI) -> AsyncClient:
    async with AsyncClient(
            app=rollback_pool,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()
