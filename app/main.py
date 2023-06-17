from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .authentication.router import router as auth_router
from .stream.router import router as stream_router
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(stream_router, prefix="/stream", tags=["Stream"])
