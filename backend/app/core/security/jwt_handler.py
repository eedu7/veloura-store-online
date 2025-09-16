from typing import Any, Dict, Literal
from uuid import uuid4

from core.config import config
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from utils import get_timestamp


class JWTHandler:
    SECRET_KEY: str = config.JWT_SECRET_KEY
    ALGORITHM: str = config.JWT_ALGORITHM
    ACCESS_EXPIRY_MINUTES: int = config.JWT_ACCESS_EXPIRY_MINUTES
    REFRESH_EXPIRY_MINUTES: int = config.JWT_REFRESH_EXPIRY_MINUTES

    @classmethod
    def encode(
        cls,
        payload: Dict[str, Any],
        token_type: Literal["access", "refresh"] = "access",
    ) -> str:
        to_encode = payload.copy()
        to_encode.update({"iat": get_timestamp()})

        if token_type == "access":
            to_encode.update({"token_type": "access", "exp": get_timestamp(minutes=cls.ACCESS_EXPIRY_MINUTES)})
        elif token_type == "refresh":
            to_encode.update(
                {"token_type": "refresh", "jti": str(uuid4()), "exp": get_timestamp(minutes=cls.REFRESH_EXPIRY_MINUTES)}
            )

        return jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

    @classmethod
    def decode(cls, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                cls.SECRET_KEY,
                algorithms=[cls.ALGORITHM],
            )

        except ExpiredSignatureError:
            raise ValueError("Expired token")
        except JWTClaimsError:
            raise ValueError("Invalid token claims")
        except JWTError:
            raise ValueError("Invalid JWT token")

        if payload.get("token_type") not in {"access", "refresh"}:
            raise ValueError("Unknown token type")
        return payload
