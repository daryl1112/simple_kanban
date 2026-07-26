# DevBoard API (backend)

FastAPI service that is the system of record for the DevBoard Kanban tool. Every
board action is a REST endpoint, so anything the UI can do is scriptable.

## Structure

```
app/
├── main.py            # app factory, logging middleware, router registration
├── core/              # config, logging, database (cross-cutting concerns)
├── models/            # SQLAlchemy ORM models (one file per entity)
├── schemas/           # Pydantic request/response models
├── services/          # business logic (single responsibility per module)
└── api/
    ├── deps.py        # domain-error -> HTTP translation
    └── routes/        # one router per resource
tests/                 # pytest suite mirroring the app package
```

The layering is routes -> services -> models. Routes never touch the database
directly; services never raise HTTP errors. Domain exceptions
(`NotFoundError`, `ValidationError`) are translated to HTTP status codes in the
route layer.

## Configuration

All settings come from environment variables (see `../.env.example`):

| Variable       | Default                        | Purpose                       |
| -------------- | ------------------------------ | ----------------------------- |
| `DATABASE_URL` | `sqlite:///./devboard.db`      | SQLAlchemy connection string  |
| `LOG_LEVEL`    | `INFO`                         | Root log level                |
| `CORS_ORIGINS` | `http://localhost:3000`        | Comma-separated allowed origins |

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Interactive API docs (OpenAPI/Swagger) are then served at
`http://localhost:8000/docs`.

## Tests

```bash
pytest
```

Tests run against an isolated in-memory SQLite database — no external services
required.

## Key endpoints

- `POST /projects`, `GET /projects/{id}`, `GET /projects/{id}/board`
- `POST /projects/{id}/cards`, `PATCH /cards/{id}` (move / assign / edit)
- `POST /cards/{id}/dependencies` (cycle-checked), `DELETE /cards/{id}/dependencies/{dep_id}`
- `POST /cards/{id}/comments` (Markdown), `DELETE /comments/{id}`
- `POST /users`, `GET /users`
