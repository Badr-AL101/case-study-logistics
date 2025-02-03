FROM python:3.10.12-slim

RUN apt-get update && \
apt-get install -y ssh iputils-ping vim && \
mkdir /var/run/sshd && \
chmod 0755 /var/run/sshd && \
apt-get --purge autoremove && \
apt-get -y clean
# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY src/ .

CMD ["./startup.sh"] 
# CMD ["python","test_connection.py"]
