# Start with an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Also install MySQL client development libraries needed for mysqlclient
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc &&     pip install --no-cache-dir -r requirements.txt &&     apt-get purge -y --auto-remove default-libmysqlclient-dev gcc &&     rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
# Add a placeholder for DATABASE_URL, to be overridden by docker-compose
ENV DATABASE_URL="mysql+mysqlclient://user:password@db/myapp_db"
ENV SECRET_KEY="a-very-secret-key-for-docker" # Should be overridden in production

# Run the application
# Use gunicorn for a production-ready server
# RUN pip install gunicorn # Install gunicorn
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
# For development, Flask's built-in server can be used:
CMD ["flask", "run"]
