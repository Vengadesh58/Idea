from jose import JWSError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key
# algorithm
# expiration time of the token


SCERET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e71"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SCERET_KEY, algorithm=[ALGORITHM])

    return encoded_jwt


def verify_acces_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SCERET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("user_email")

        if email in None:
            raise credentials_exception

        token_data = schemas.TokenData(email=email)

    except JWSError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="could not validate credentials", headers={"WWW-Authenticate": "bearer"})
    return verify_acces_token(token, credentials_exception)
