# Pull base image
FROM python:3.11
# 
WORKDIR /code
# 
COPY ./requirements.txt /code/requirements.txt
# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# 
COPY ./app /code/app
# 
#CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class",  "uvicorn.workers.UvicornWorker", "--bind", "localhost:8080"]

EXPOSE 8000