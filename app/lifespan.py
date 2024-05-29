from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def task_runner(app: FastAPI):
    # Code to run at startup
    print("task running...")
    yield
    # Code to run at shutdown
    # (e.g., cleanup resources if needed)
