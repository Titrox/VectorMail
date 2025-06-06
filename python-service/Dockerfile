FROM python:3.10

WORKDIR /app

# Copy relevant files to container
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "fine_tuning.py"]
