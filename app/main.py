from fastapi import FastAPI

from app.core.config import get_settings
from app.core.lifespan.contex_manager import lifespan
from app.web.router import main_router


class Application:
    app: FastAPI

    def __init__(self):
        self._config = get_settings()
        self.create_app().include_router().set_lifespan()

    def __call__(self, *args, **kwargs):
        return self.app

    def create_app(self):
        self.app = FastAPI(
            **self._config.fastapi_settings,
            lifespan=lifespan,
        )
        return self

    def include_router(self):
        self.app.include_router(main_router)
        return self

    def set_lifespan(self):
        return self


app = Application()()
