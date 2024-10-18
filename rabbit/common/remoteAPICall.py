import logging
import httpx


log = logging.getLogger(__name__)


def create_user_in_fastapi(
    user_data: dict,
):
    with httpx.Client() as client:
        response = client.post(
            "http://127.0.0.1:8001/auth/register",
            json={
                "email": user_data["email"],
                "password": user_data["password"],
            },
        )
        log.warning(f"Created new user {user_data["email"]}. Message from django")

        return response.json()
