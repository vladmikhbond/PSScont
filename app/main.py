from fastapi import FastAPI
from .routers import api_router, token_router

app = FastAPI()

app.include_router(token_router.router, prefix="", tags=["token"])
app.include_router(api_router.router, prefix="/api", tags=["problem"])

