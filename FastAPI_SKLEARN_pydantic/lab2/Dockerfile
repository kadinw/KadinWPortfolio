# ---------- Builder Stage ----------
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y \
         curl \
         build-essential \
         libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create venv first
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy only dependency files first for caching
COPY pyproject.toml poetry.lock /app/

# Install Poetry in the SYSTEM python (not the venv), export requirements,
# then install deps INTO the venv using pip.
RUN python -m pip install --no-cache-dir "poetry==2.3.2" "poetry-plugin-export==1.8.0" \
    && poetry export --without dev --format requirements.txt --output /tmp/requirements.txt --without-hashes \
    && /venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
    && python -m pip uninstall -y poetry poetry-plugin-export \
    && rm -rf /root/.cache /tmp/requirements.txt

# Copy your app source last
COPY . /app

# Optional: prune venv (safe)
RUN find /venv -type d -name "__pycache__" -prune -exec rm -rf {} + \
 && find /venv -type f -name "*.pyc" -delete \
 && find /venv/lib/python3.13/site-packages -type d \( -name "tests" -o -name "test" \) -prune -exec rm -rf {} + \
 && find /venv/lib/python3.13/site-packages -type f -name "*.so" -exec strip --strip-unneeded {} + 2>/dev/null || true

# ---------- Runtime Stage ----------
FROM python:3.13-slim

WORKDIR /app

# Copy only the venv + app into runtime (not the whole /usr/local)
COPY --from=builder /venv /venv
COPY --from=builder /app /app

ENV PATH="/venv/bin:$PATH"

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]