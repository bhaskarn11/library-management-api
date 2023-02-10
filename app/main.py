from fastapi import FastAPI
from .database import engine
from . import models
from .routers import items, users

models.Base.metadata.create_all(engine)

app = FastAPI(
    title="Library Management API",
    version="0.0.1"
)

app.include_router(items.router)
app.include_router(users.router)

# @app.get("/")
# def root():
#     return {"Hello": "World"}
