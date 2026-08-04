# DevBoard

An in-house, Trello-style Kanban tool for software development. Create projects,
work cards across five columns (Backlog → Approved → In Progress → Review →
Completed), assign owners, declare dependencies between cards, track sub-tasks with
checklists, and leave Markdown comments. **Every action is available both in the UI and via the REST
API** — the UI is simply a client of that API.

## Architecture

Three containers orchestrated by Docker Compose:

```
┌────────────┐     REST/JSON      ┌────────────┐      SQL       ┌────────────┐
│  frontend  │ ─────────────────▶ │  backend   │ ─────────────▶ │  Postgres  │
│  Next.js   │                    │  FastAPI   │                │            │
└────────────┘                    └────────────┘                └────────────┘
   :3000                             :8000                          :5432
```

- **backend/** — FastAPI service, the system of record. Auto-generated OpenAPI
  docs at `/docs`. Layered as routes → services → models.
- **frontend/** — Next.js App Router UI (board, drag-and-drop, card editor).
- **db** — PostgreSQL with a persisted volume.

Each service is self-contained with its own `Dockerfile` and `README.md`,
following a microservices-style layout. No container is given an explicit name.

## Quick start

```bash
cp .env.example .env          # optional; sensible defaults are built in
docker compose up --build
```

Then open:

- UI — http://localhost:3000
- API docs (Swagger UI) — http://localhost:8000/docs
- Health check — http://localhost:8000/health

## Data model

| Entity      | Notes                                                             |
| ----------- | ---------------------------------------------------------------- |
| Project     | Owns a board. Markdown description.                              |
| Card        | title, Markdown description, status, optional assignee.         |
| Dependency  | Card → card, same project, **acyclic (server-enforced)**.       |
| Checklist   | Named task list on a card; items have completable checkboxes.   |
| Comment     | Markdown body on a card, optional author.                       |
| User        | A person a card can be assigned to (no auth — in-house tool).    |

## API highlights

| Action              | Endpoint                                    |
| ------------------- | ------------------------------------------- |
| Create project      | `POST /projects`                            |
| Get board           | `GET /projects/{id}/board`                  |
| Create card         | `POST /projects/{id}/cards`                 |
| Move / assign / edit| `PATCH /cards/{id}`                         |
| Add dependency      | `POST /cards/{id}/dependencies`             |
| Remove dependency   | `DELETE /cards/{id}/dependencies/{dep_id}`  |
| Comment on a card   | `POST /cards/{id}/comments`                 |
| Add a checklist     | `POST /cards/{id}/checklists`               |
| Add a checklist item| `POST /checklists/{id}/items`               |
| Toggle an item      | `PATCH /checklist-items/{id}`               |

Full, interactive documentation is generated automatically at `/docs`.

## Development & tests

Both services are independently testable.

```bash
# Backend
cd backend && pip install -r requirements.txt && pytest

# Frontend
cd frontend && npm install && npm test
```

## Repository layout

```
devboard/
├── backend/            # FastAPI service (app/, tests/, Dockerfile, README)
├── frontend/           # Next.js app (app/, components/, lib/, __tests__/)
├── docker-compose.yml  # three services; no container_name set
├── .env.example
└── README.md
```

## Design notes

- **Separation of concerns.** The backend keeps HTTP, business logic, and
  persistence in distinct layers; domain errors are translated to HTTP codes at
  the edge. The frontend keeps API access (`lib/api`) separate from presentation
  (`components`).
- **Config via environment.** No secrets or environment-specific values are
  hard-coded; everything flows through env vars and `.env`.
- **Dependency safety.** The API rejects self-dependencies, cross-project
  dependencies, and any edge that would introduce a cycle.
