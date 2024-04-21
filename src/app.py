from fastapi import FastAPI
from .api import router
from .settings import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(router)


origins = [
    f"http://{settings.front_end_host}:{settings.front_end_port}",
    f"http://{settings.front_end_host}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)