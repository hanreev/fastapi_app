from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database.models import create_db_and_tables
from .middleware.process_time import ProcessTimeMiddleware
from .routes import items, users

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ProcessTimeMiddleware)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"message": "Hello World"}


app.include_router(users.router)
app.include_router(items.router)
