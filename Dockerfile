# ─────────────────────────────────────────────────────────
# BASE
FROM python:3.10-slim

# Set build arguments
ARG GITHUB_TOKEN
ARG GITHUB_USER
ARG FORGEN_REPO
ARG USPTO_DATA_REPO

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# ─────────────────────────────────────────────────────────
# Install base dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ─────────────────────────────────────────────────────────
# Clone & install private repos
RUN git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${FORGEN_REPO}.git /git_tmp/forgen && \
    pip install /git_tmp/forgen && \
    rm -rf /git_tmp/forgen

RUN git clone https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${USPTO_DATA_REPO}.git /git_tmp/uspto_data && \
    pip install /git_tmp/uspto_data && \
    rm -rf /git_tmp/uspto_data

# ─────────────────────────────────────────────────────────
# Copy application code
COPY . /app

# ─────────────────────────────────────────────────────────
# Run your FastAPI app (or change this as needed)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
