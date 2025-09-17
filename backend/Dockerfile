## ------------------------------- Builder Stage ------------------------------ ##
FROM python:3.13-bookworm AS buider

RUN apt-get update && apt-get install --no-install-recommends -y \
    gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod +x /install.sh && /install.sh && rm /install.sh

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY ./app/pyproject.toml ./app/uv.lock* /app/

RUN uv sync --frozen

## ------------------------------- Production Stage ------------------------------ ##
FROM python:3.13-slim-bookworm AS production

WORKDIR /app
COPY /app .
COPY --from=builder /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8080"]