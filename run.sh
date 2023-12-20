#! /bin/bash
poetry run uvicorn transcriptor.main:app --host 0.0.0.0 --port 8000
