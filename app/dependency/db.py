from fastapi import Request

from asyncpg import Pool, Connection


async def get_connection(request: Request) -> Connection:
    pool: Pool = request.app.state.pool
    async with pool.acquire() as connection:
        yield connection
