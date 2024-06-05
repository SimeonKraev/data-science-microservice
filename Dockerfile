# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Copy csvs into the Docker image
COPY employees/us.csv .
COPY employees/uk.csv .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app to run on
EXPOSE 5000

# Set environment variable to tell Flask to run in production mode
ENV FLASK_APP=brain.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the command to start the Flask server
CMD ["flask", "run"]