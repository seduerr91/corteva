# Start from the fastapi image.
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Select folder with code
WORKDIR /app

#  Copy requirements file
COPY requirements.txt app/requirements.txt

# Install requirements 
RUN pip install --no-cache-dir --upgrade -r app/requirements.txt


# Copy files
COPY . /app

# Run server and expose port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

