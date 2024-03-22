# Use an official Python runtime as a parent image
FROM python:3.12.1-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies
# For pygame and other libraries, you might need additional dependencies
RUN apt-get update && apt-get install -y \
    python3-pygame \
    libgl1-mesa-dev \
    libglib2.0-0 \
    libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
# EXPOSE 8000 (Uncomment this if you need to expose any port, e.g., for a web server)

# Run script.py when the container launches
# Replace 'script.py' with the name of your main script file
CMD ["python", "./prl_26.py", "A", "co_ba_1999_03_23_333_f", "Y"]
