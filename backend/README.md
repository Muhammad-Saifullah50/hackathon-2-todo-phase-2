# Todo API Backend

FastAPI-based backend for the Todo Application.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.13
- **Database**: PostgreSQL (Neon) via SQLModel (SQLAlchemy + Pydantic)
- **Migrations**: Alembic
- **Package Manager**: uv
- **Testing**: pytest

## Setup

### Prerequisites

- Python 3.13+
- uv (recommended) or pip

### Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   # OR
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Update `DATABASE_URL` with your Neon connection string.

3. **Run the server**:
   ```bash
   # Using uv
   uv run uvicorn src.main:app --reload

   # OR directly
   uvicorn src.main:app --reload
   ```

   The API will be available at http://localhost:8000.
   Docs: http://localhost:8000/docs

## Testing

Run tests with pytest:
```bash
uv run pytest
```

To run tests with coverage:
```bash
uv run pytest --cov=src --cov-report=term-missing
```

To run tests in watch mode (requires pytest-watch):
```bash
uv run ptw
```

## Code Quality

Maintain code standards with the following commands:

- **Linting**: `uv run ruff check src/ tests/`
- **Formatting**: `uv run black src/ tests/`
- **Type Checking**: `uv run mypy src/ tests/`
- **All-in-one check**: `poe check` (if using poethepoet)

## Docker

Run using Docker Compose from the root directory:
```bash
docker-compose up backend
```
