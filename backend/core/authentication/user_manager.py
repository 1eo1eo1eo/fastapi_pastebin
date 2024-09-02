from typing import Optional, TYPE_CHECKING

from fastapi_users import BaseUserManager, IntegerIDMixin

import logging

from auth.dependencies.models import User
from core.config import settings
from tasks.tasks import (
    send_email_password_reset_token,
    send_email_registration_verify_token,
)

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        send_email_password_reset_token.delay(
            token=token,
            email_address=user.email,
        )
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        send_email_registration_verify_token.delay(
            token=token,
            email_address=user.email,
        )
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )
