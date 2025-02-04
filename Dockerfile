FROM python:3.10.12-slim

RUN apt-get update && \
apt-get install -y ssh iputils-ping vim && \
mkdir /var/run/sshd && \
chmod 0755 /var/run/sshd && \
apt-get --purge autoremove && \
apt-get -y clean
# Set the working directory in the container
WORKDIR /usr/app/src

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
COPY requirements_dev.txt ./
RUN pip install -r requirements.txt
# RUN pip install -r requirements_dev.txt

COPY src/ .

COPY data/ /usr/app/data

COPY ssh_config/sshd_config /etc/ssh/sshd_config

CMD ["./startup.sh"] 
# CMD ["jupyter", "notebook", "--ip=*", "--port=8888", "--allow-root","--no-browser"]
# CMD ["python","test_connection.py"]
