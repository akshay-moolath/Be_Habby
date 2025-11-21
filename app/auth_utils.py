from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = "change_this_before_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24




def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)




def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)