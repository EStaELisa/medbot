# Use the official Python 3.10 image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies without using cache to reduce image size
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the entire FastAPI backend code into the container
COPY . /code/fastapi_backend

# Define the command to run the FastAPI applicated on port 80
CMD ["fastapi", "run", "fastapi_backend/app/main.py", "--port", "80"]