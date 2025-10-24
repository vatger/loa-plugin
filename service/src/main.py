from fastapi import FastAPI

from api.router import router

app = FastAPI(
    title="LoA Service",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "LoA Service running!"}
