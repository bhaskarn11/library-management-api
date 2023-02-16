from fastapi import FastAPI
from .database import engine
from . import models
from .routers import items, users

models.Base.metadata.create_all(engine)

DESCRIPTION = """
    This is a REST API for library managment, developed using Python and FastAPI
    it was created as an excersise 
"""

app = FastAPI(
    title="Library Management API",
    description=DESCRIPTION,
    contact={"Github": "github.com/bhaskarn11"},
    version="1.0.1"
)

app.include_router(items.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"details": "Goto to path /docs for API documentation"}
