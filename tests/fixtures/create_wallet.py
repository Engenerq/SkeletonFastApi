import pytest
from asyncpg import Pool


@pytest.fixture
def create_new_wallet(pool: Pool):
    async def create() -> dict:
        query = """
            insert into wallets (amount)
            values (0)
            RETURNING *;
        """
        async with pool.acquire() as conn:
            return dict(await conn.fetchrow(query))

    return create
