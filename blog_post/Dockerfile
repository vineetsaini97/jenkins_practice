# Use the official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /api_data

# Copy the requirements file to the working directory
COPY requirements.txt /api_data/requirements.txt

# Install the Python dependencies
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "crud_api:app", "--host", "0.0.0.0", "--port", "8000"]