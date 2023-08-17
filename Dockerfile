FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN pip install --no-cache-dir --upgrade -r requirements.txt
