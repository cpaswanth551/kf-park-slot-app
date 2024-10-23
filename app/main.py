from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import users, auth, parks, reservations
from .db.base import Base, engine


app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(parks.router)
app.include_router(reservations.router)


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
