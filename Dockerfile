# set base image (host OS)
FROM python:3.8-slim-buster

# set the working directory in the container
WORKDIR /crystalline

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY crystalline/ .

EXPOSE 5002

# command to run on container start
CMD [ "python", "./main.py" ] 