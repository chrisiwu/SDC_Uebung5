FROM python:3.8
# set the base image
# since we're running # a Python application
# a Python base image is used FROM python:3.8
# set a key-value label for the Docker image
LABEL maintainer="chrisiwu"
# copy files from the host to the container filesystem
# for example, all the files in the current directory
# to the  '/app' directory in the container
COPY . /app
#  defines the working directory within the container
WORKDIR /app
# run commands within the container
# for example, invoke a pip command 
# to install dependencies defined in the requirements.txt file
RUN pip install -r requirements.txt
# provide a command to run on container start
# for example, start the 'app.py' application
CMD ["streamlit", "run", "app.py"]