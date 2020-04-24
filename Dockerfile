# Use an official Python runtime as an image
FROM python:3.6

# The EXPOSE instruction indicates the ports on which a container
# will listen for connections
# Since Flask apps listen to port 5000 by default, we expose it
EXPOSE 5000

# Now, add all the current files to codev directory
ADD . /codev

# Notice we haven't created a directory by this name - this instruction
# creates a directory with this name if it doesn't exist
WORKDIR /codev

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt