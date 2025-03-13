import http

from fastapi import Depends, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBase
from telegram_webapp_auth.auth import (
    TelegramAuthenticator,
    WebAppUser,
    generate_secret_key,
)
from telegram_webapp_auth.errors import InvalidInitDataError

from config import settings

telegram_authentication_schema = HTTPBase()


def get_telegram_authenticator() -> TelegramAuthenticator:
    secret_key = generate_secret_key(settings.telegram.token.get_secret_value())
    return TelegramAuthenticator(secret_key)


def get_current_user(
    auth_cred: HTTPAuthorizationCredentials = Depends(telegram_authentication_schema),
    telegram_authenticator: TelegramAuthenticator = Depends(get_telegram_authenticator),
) -> WebAppUser:
    try:
        init_data = telegram_authenticator.validate(auth_cred.credentials)
    except InvalidInitDataError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden access.",
        )
    except Exception:
        raise HTTPException(
            status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal error.",
        )

    if init_data.user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden access.",
        )

    return init_data.user
