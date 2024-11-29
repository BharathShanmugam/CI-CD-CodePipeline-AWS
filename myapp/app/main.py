from fastapi import FastAPI
from .model import Base
from db import engine
from .api import router

Base.metadata.create_all(bind=engine)  # Create database tables

app = FastAPI()

app.include_router(router, prefix="/api")
