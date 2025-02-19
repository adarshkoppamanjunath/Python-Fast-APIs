from fastapi import FastAPI, Request
from app.docs.custom_docs import custom_openapi
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.database import *

app = FastAPI(
    title="My FastAPI Project",
    description="API Documentation divided into different sections for better readability.",
    version="1.0.0"
)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
#setup databse will add two users to get token and also initialize db for basic auth

def include_router():
    from app.routes import basic_auth
    from app.routes import jwt_auth
    app.include_router(basic_auth.router)
    app.include_router(jwt_auth.router)
# Custom OpenAPI schema
app.openapi = custom_openapi(app)
setup_db()
include_router()
@app.exception_handler(RateLimitExceeded)
async def rate_limit_error(request: Request, exc: RateLimitExceeded):
    # Respond with a custom JSON error message
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Please try again later."}
    )