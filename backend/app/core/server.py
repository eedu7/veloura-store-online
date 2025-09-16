from contextlib import asynccontextmanager

from api import router
from core.session import Base, engine
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(lifespan=lifespan)

    app_.include_router(router)

    return app_


app = create_app()
