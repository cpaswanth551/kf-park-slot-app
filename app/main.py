from fastapi import FastAPI

from .api.v1 import users, auth
from .db.base import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)


@app.get("/health-check")
def headCheck():
    return {"message": "all is well.."}
