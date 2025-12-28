# Stage 1: Builder - Install dependencies
FROM python:3.11-slim-bookworm as builder

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to the terminal
ENV PYTHONUNBUFFERED 1

# Install build dependencies and then application dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Final - Create the production image
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Create a non-root user
RUN addgroup --system --gid 1001 nobody && \
    adduser --system --uid 1001 --gid 1001 nobody

# Copy dependencies from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copy application code
COPY app.py .

# Switch to the non-root user
USER nobody

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers=4", "app:app"]
