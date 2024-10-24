from contextlib import asynccontextmanager
from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_app.router.cmd import router as cmd_router
from redis_app.version import __version__


origin = getenv("ORIGIN", "*")

app = FastAPI(title="Redis APP", description="Redis APP", version=__version__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    except Exception as e:
        raise e
    finally:
        pass


dependencies = []
app.include_router(
    cmd_router,
    dependencies=dependencies
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return True
