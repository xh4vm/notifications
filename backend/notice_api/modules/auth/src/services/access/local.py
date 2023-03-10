import hashlib
from typing import Any, Literal, Optional, Union

import jwt
from modules.auth.core.config import CONFIG, auth_logger
from modules.auth.src.errors.permission import PermissionError
from modules.auth.src.errors.token import TokenError

from .base import BaseAccessService


class AccessService(BaseAccessService):
    def is_accessible(
        self, token: str, method: str, url: str
    ) -> dict[Literal['is_accessible', 'message', 'payload'], Union[bool, str, dict[str, Any]]]:

        try:
            payload = jwt.decode(jwt=token, key=CONFIG.APP.JWT_SECRET_KEY, algorithms=CONFIG.APP.JWT_DECODE_ALGORITHMS)

        except jwt.exceptions.InvalidSignatureError:
            auth_logger.info(TokenError.INVALIDED_SIGNATURE_ERROR)
            return self._wrapper(status=False, message=TokenError.INVALIDED_SIGNATURE_ERROR)

        except jwt.exceptions.ExpiredSignatureError:
            auth_logger.info(TokenError.EXPIRED_SIGNATURE_ERROR)
            return self._wrapper(status=False, message=TokenError.EXPIRED_SIGNATURE_ERROR)

        except jwt.exceptions.DecodeError:
            auth_logger.info(TokenError.DECODE_ERROR)
            return self._wrapper(status=False, message=TokenError.DECODE_ERROR)

        permissions = payload.get('permissions')

        if permissions is None:
            auth_logger.info(TokenError.FORMAT_ERROR)
            raise ValueError(TokenError.FORMAT_ERROR)

        md5_hashed_url = hashlib.md5(url.encode(), usedforsecurity=False).hexdigest()

        if isinstance((allowed_methods := permissions.get(md5_hashed_url)), list) and method in allowed_methods:
            auth_logger.info(PermissionError.ACCESS_SUCCESS)
            return self._wrapper(status=True, message=PermissionError.ACCESS_SUCCESS, payload=payload)

        auth_logger.info(PermissionError.ACCESS_ERROR)
        return self._wrapper(status=False, message=PermissionError.ACCESS_ERROR)

    def _wrapper(
        self, status: bool, message: str, payload: Optional[dict[str, Any]] = None
    ) -> dict[Literal['is_accessible', 'message', 'payload'], Union[bool, str, dict[str, Any]]]:
        return {'is_accessible': status, 'message': message, 'payload': payload}
