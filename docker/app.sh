#!/bin/bash

cd /app/backend

alembic upgrade head

poetry run python3 run_main.py