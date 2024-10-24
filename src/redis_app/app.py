"""
This module initializes the FastAPI application for the Redis APP,
including middleware configuration and router inclusion.
"""

from contextlib import asynccontextmanager
from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from redis_app.router.cmd import router as cmd_router
from redis_app import __version__

origin = getenv("ORIGIN", "*")

app = FastAPI(title="Redis APP", description="Redis APP", version=__version__)


@asynccontextmanager
async def lifespan():
    """
    Lifespan context manager for the FastAPI application.

    This function manages startup and shutdown events for the application.
    """
    try:
        yield
    except Exception as e:
        raise e
    finally:
        pass


dependencies = []
app.include_router(cmd_router, dependencies=dependencies)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple boolean value.

    This can be used to verify that the service is running.
    """
    return True
