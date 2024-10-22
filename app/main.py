from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import users, auth, parks
from .db.base import Base, engine


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(parks.router)


@app.get("/health-check")
def headCheck():
    return {"message": "all is well.."}


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
