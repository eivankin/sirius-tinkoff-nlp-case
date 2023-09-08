FROM python:3.10-alpine AS builder

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine AS development
COPY --from=builder /opt/venv /opt/venv

# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app
COPY . .
CMD ["python", "main.py"]