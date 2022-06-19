import hashlib

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.database.schemas.user import User, UserCreate
from app.database.services import user

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def password_to_md5(password: str):
    return hashlib.md5(password.encode('utf-8')).hexdigest()


async def retrieve_user(token: str = Depends(oauth2_scheme)):
    auth_user = await user.get(token)
    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_user


async def retrieve_active_user(current_user: User = Depends(retrieve_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    auth_user = await user.get(form.username)
    if not auth_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not auth_user.password == password_to_md5(form.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": auth_user.login, "token_type": "bearer"}


@router.post("/registration", response_model=User)
async def registration(form_user: UserCreate):
    auth_user = await user.get(form_user.login)
    if auth_user:
        raise HTTPException(status_code=400, detail="Login exists")
    form_user.password = password_to_md5(form_user.password)
    query = await user.post(form_user)
    return query
