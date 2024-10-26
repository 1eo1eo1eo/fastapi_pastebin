from core.gunicorn import (
    Application,
    get_app_options,
)
from main import main_app
from core.config import settings


def main():
    Application(
        application=main_app,
        options=get_app_options(
            host=settings.gunicorn.host,
            port=settings.gunicorn.port,
            workers=settings.gunicorn.workers,
            timeout=settings.gunicorn.timeout,
            log_level=settings.logging.log_level,
        ),
    ).run()


if __name__ == "__main__":
    main()
