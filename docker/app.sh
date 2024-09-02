#!/bin/bash

cd backend

alembic upgrade head

gunicorn main:main_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000