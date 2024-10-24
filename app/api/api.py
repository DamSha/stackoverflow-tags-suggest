from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import base, predict
from .config import settings

# models.Base.metadata.create_all(bind=engine)
description = """
# API de suggestion de Tags sur une question de Stackoverflow.
## Usage
- 🚀 POST to **/predict/tags**
    - with body/message
## Author
- Damien Chauvet
"""
app = FastAPI(
    title="API Stackoverflow - Tags predictions",
    description=description,
    version="0.2.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(base.router)
app.include_router(predict.router)
