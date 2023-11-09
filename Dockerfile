# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container at /code/
COPY ./requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code/
COPY . /code/

# Expose port 8000 to allow communication to/from server
EXPOSE 8000

# Define the command to run the application
CMD ["gunicorn", "-b", "0.0.0.0:8000", "core.wsgi:application"]

