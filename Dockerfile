# Stage 1: Build environment (install dependencies)
FROM python:3.11-slim as builder

WORKDIR /app

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/python -r requirements.txt

# Copy source code
COPY app/ .

# Stage 2: Distroless image
FROM gcr.io/distroless/python3-debian11

# Set working directory
WORKDIR /app

# Copy installed site-packages and source code from builder
COPY --from=builder /python /python
COPY --from=builder /app /app

# Set Python path so it can find packages
ENV PYTHONPATH=/python

# Specify the command
CMD ["main.py"]
