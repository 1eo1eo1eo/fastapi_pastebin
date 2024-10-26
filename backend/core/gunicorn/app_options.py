from core.gunicorn.logger_class import GunicornLogger


def get_app_options(
    host: str,
    port: int,
    workers: int,
    timeout: int,
    log_level: str,
) -> dict:
    return {
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": GunicornLogger,
        "log_level": log_level,
        "bind": f"{host}:{port}",
        "workers": workers,
        "timeout": timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
