# FastAPI Auth JWT + Role

## Run DB

docker compose up -d

## Setup venv

python -m venv .venv

# activate .venv (Windows)

.\.venv\Scripts\Activate.ps1

## Install deps

python -m pip install -r requirements.txt

## Init DB

python -m app.scripts.init_db

## Run API

uvicorn app.main:app --reload
