# Use the public Amazon Linux 2 image as a base.
FROM python:3.10-slim

# Install the required packages.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy your application code.
COPY main.py ./

# Command to run the FastAPI app using Mangum handler.
CMD ["main.handler"]
