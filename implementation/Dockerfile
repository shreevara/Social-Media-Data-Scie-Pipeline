# Use the official Python 3.9 image as the base image
FROM python:3.9

# Set up a working directory inside the container
WORKDIR /app

# Copy your application code and requirements file into the container
COPY . .

# Install your Python dependencies
RUN pip install -r requirements.txt

# Run your Python script
CMD python3 reddit_comments.py & python3 thread.py