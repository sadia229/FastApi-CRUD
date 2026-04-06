from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database import Base, engine
from infrastructure.database import models  # noqa: F401
from presentation.routers.users import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Clean Architecture User API", lifespan=lifespan)
app.include_router(users_router)


@app.get("/", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
