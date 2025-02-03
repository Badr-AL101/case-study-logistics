FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/test_connection.py .

CMD ["python","test_connection.py"]
