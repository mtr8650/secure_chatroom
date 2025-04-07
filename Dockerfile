# Use official Python image
FROM hub.hamdocker.ir/python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files first
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry lock && poetry install --no-root
    

# Copy the entire project
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "uvicorn", "chat_room.main:app", "--host", "0.0.0.0", "--port", "8000"]
