ARG PYTHON_VERSION=3.14

FROM python:${PYTHON_VERSION}-slim AS builder

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:${PYTHON_VERSION}-slim AS runtime

LABEL org.opencontainers.image.title="Klima API" \
      org.opencontainers.image.description="FastAPI backend for Klima IoT telemetry and control" \
      org.opencontainers.image.source="https://github.com/Mulekotd/klima-iot"

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN groupadd --system klima \
    && useradd --system --gid klima --home-dir /app klima

COPY --from=builder /opt/venv /opt/venv
COPY --chown=klima:klima app ./app

USER klima

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen(f\"http://127.0.0.1:{os.getenv('PORT', '8000')}/health\", timeout=3)"]

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
