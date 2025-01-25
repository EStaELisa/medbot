FROM python:3.10
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code/fastapi_backend
CMD ["fastapi", "run", "fastapi_backend/app/main.py", "--port", "80"]