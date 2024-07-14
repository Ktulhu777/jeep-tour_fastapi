#!/usr/bin/env sh

alembic upgrade head

uvicorn app:app --reload --host=0.0.0.0 --port=8000