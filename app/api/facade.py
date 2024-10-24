from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.api.routers import base, predict
from app.api.config import settings

api_version = "0.1.2"
api_description = """
## Usage
- 🚀 POST to **/predict/tags**
    - with body/message
## Author
- Damien Chauvet
"""
api_origins = ["*"]

app = FastAPI(
    title="API Stackoverflow - Tags predictions",
    description=api_description,
    version=api_version,
)

# Add Rate Limiter
# Max 3/sec : 1 token_expired + 1 get_token + 1 API call
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["3/second"],
                  )
# limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# Add Limiter Globally
# Send 429 status with details {"error":"Rate limit exceeded: 1 per 1 second"}

# Apply Middlewares
app.add_middleware(
    SlowAPIMiddleware,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=api_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(base.router)
app.include_router(predict.router)
