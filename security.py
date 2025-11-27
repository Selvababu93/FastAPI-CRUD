from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = "02e3f7f0508fe15b9f551ce3226d59073ec7a1c91da6ad6bc0b8bad17731b437"
ALGORITHM = "HS256"



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def hash_password(password: str):
    return bcrypt_context.hash(password)



def verify_password(password: str, hashed_password: str):
    return bcrypt_context.verify(password, hashed_password)



def create_access_token(username: str, user_id : int, user_role: str, expires_delta: timedelta):
    to_encode = {"sub" : username, "id" : user_id, "role" : user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp" : int(expires.timestamp())})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        
        if not username or not user_id or not user_role :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request")
        
        return {"username" : username, "id" : user_id, "user_role" : user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    

user_dependency = Annotated[dict, Depends(get_current_user)]