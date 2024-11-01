from fastapi import FastAPI

from contextlib import AbstractAsyncContextManager


class BaseLifespanManager(AbstractAsyncContextManager):
    async def start(self):
        return NotImplementedError()

    async def stop(self):
        return NotImplementedError

    def __init__(self, app: FastAPI):
        self.app = app
        self.state = {}

    def __await__(self):
        yield self

    def keys(self):
        return self.state.keys()

    async def __aenter__(self):
        self.state.update(await self.start())

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
        self.state.clear()

    def __getitem__(self, item):
        return self.state[item]

    def __iter__(self):
        yield from self.state.keys()
