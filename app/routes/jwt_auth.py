from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Request
from fastapi import APIRouter
from slowapi.util import get_remote_address
from app.models.basemodel import *
from app.utils.utils import *
from app.db.database import *
from app.main import limiter

router = APIRouter(tags=["JWTAuth"])


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        print(user)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.get("/secure-data-jwt-view")
@limiter.limit("5/minute")
async def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    return {"Username": current_user}

@router.get("/secure-data-jwt-admin")
@limiter.limit("5/minute")
async def read_users_me(request: Request, current_user: User = Depends(get_current_user), role: str = Depends(require_role_jwt("admin"))):
    return {"Username": current_user}