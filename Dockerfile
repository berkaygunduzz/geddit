# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9.6

# Allows docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Mounts the application code to the image
COPY . code
WORKDIR /code

EXPOSE 8000

# runs the production server
RUN python3 src/geddit/manage.py makemigrations
RUN python3 src/geddit/manage.py migrate

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

# Add the cron job
COPY geddit_crontab /etc/cron.d/geddit_crontab
RUN chmod 0644 /etc/cron.d/geddit_crontab
RUN crontab /etc/cron.d/geddit_crontab

CMD python3 src/geddit/manage.py runserver 0.0.0.0:8000