# social_network_api

## Installation and launch
1. Create and activate virtual environment: ```python3 -m venv venv``` и ```source venv/bin/activate``` (or ```venv\Scripts\activate``` on Windows)
2. Install dependencies: ```pip install -r requirements.txt```

## Running
1. Start Redis Server: ```redis-server```
2. Start FastAPI: ```uvicorn app.main:app --reload```
3. Start Celery worker: ```celery -A app.tasks.tasks worker --loglevel=info```