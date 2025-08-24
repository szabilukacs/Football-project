# Base image
FROM python:3.11-slim-buster

# create inside the container
WORKDIR /app

COPY requirements.txt .

# Install python packeges into the image
RUN pip install --no-cache-dir -r requirements.txt

# copy all to the container
COPY main.py .
COPY src/ ./src
COPY Data/ ./Data

CMD ["python", "main.py"]