# DevBoard Project Manifest

## Project Overview
DevBoard is an in-house, Trello-style Kanban tool for software development. It enables teams to create projects, manage work cards across five columns (Backlog → Approved → In Progress → Review → Completed), assign owners, declare dependencies between cards, and leave Markdown comments. Every action is available both in the UI and via the REST API.

## Directory Structure
```
devboard/
├── backend/            # FastAPI service (app/, tests/, Dockerfile, README)
├── frontend/           # Next.js app (app/, components/, lib/, __tests__/)
├── docker-compose.yml  # three services; no container_name set
├── .env.example
└── README.md
```

## Technology Stack

### Backend (Python)
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Architecture**: Layered approach (routes → services → models)
- **Testing**: pytest with in-memory SQLite database
- **Documentation**: Auto-generated OpenAPI/Swagger UI at `/docs`
- **Key Features**:
  - RESTful API endpoints for all board operations
  - Domain error handling with HTTP status code translation
  - Dependency safety (prevents self-dependencies, cross-project dependencies, and cycles)
  - Markdown support for card descriptions and comments

### Frontend (JavaScript/TypeScript)
- **Framework**: Next.js App Router with TypeScript
- **UI Components**: React-based components with drag-and-drop functionality
- **State Management**: Built-in Next.js App Router
- **Testing**: Jest + React Testing Library
- **Key Features**:
  - Drag-and-drop card movement between columns
  - Card editor with title, description (Markdown preview), status, assignee, dependencies, and comments
  - Responsive UI with Tailwind CSS styling

### Infrastructure
- **Containerization**: Docker Compose orchestrating three containers
- **Database**: PostgreSQL (port 5432)
- **Backend API**: FastAPI service (port 8000)
- **Frontend UI**: Next.js application (port 3000)

## Code Structure

### Backend Structure
```
backend/
├── app/
│   ├── main.py            # App factory, logging middleware, router registration
│   ├── core/              # Config, logging, database (cross-cutting concerns)
│   ├── models/            # SQLAlchemy ORM models (one file per entity)
│   ├── schemas/           # Pydantic request/response models
│   ├── services/          # Business logic (single responsibility per module)
│   └── api/
│       ├── deps.py        # Domain-error -> HTTP translation
│       └── routes/        # One router per resource
├── tests/                 # pytest suite mirroring the app package
├── Dockerfile
├── requirements.txt
└── README.md
```

### Frontend Structure
```
frontend/
├── app/                         # Routes (App Router)
│   ├── page.tsx                 # Projects landing
│   ├── projects/[projectId]/    # Board view
│   └── layout.tsx, globals.css  # Shell + styles
├── components/
│   ├── board/                   # Board, Column, CardItem, CardModal
│   ├── projects/                # ProjectList, CreateProjectForm
│   └── common/                  # Button, Modal, Markdown
├── lib/
│   ├── api/                     # One module per resource + fetch client
│   ├── types.ts                 # Domain types mirroring the API
│   └── constants.ts             # Status order, labels, colors
├── __tests__/                   # Jest + React Testing Library
├── Dockerfile
├── package.json
└── README.md
```

## Key API Endpoints

### Projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project details
- `GET /projects/{id}/board` - Get board view

### Cards
- `POST /projects/{id}/cards` - Create card
- `PATCH /cards/{id}` - Move/assign/edit card
- `POST /cards/{id}/dependencies` - Add dependency (cycle-checked)
- `DELETE /cards/{id}/dependencies/{dep_id}` - Remove dependency

### Comments
- `POST /cards/{id}/comments` - Add comment to card
- `DELETE /comments/{id}` - Remove comment

### Users
- `POST /users` - Create user
- `GET /users` - Get users

## Development & Testing

### Backend
```bash
cd backend && pip install -r requirements.txt && pytest
```

### Frontend
```bash
cd frontend && npm install && npm test
```

## Architecture Diagram
```
┌─────────────┐     REST/JSON      ┌─────────────┐      SQL       ┌─────────────┐
│  frontend   │ ────────────────── │   backend   │ ──────────── │  Postgres   │
│  Next.js    │                    │  FastAPI    │              │             │
└─────────────┘                    └─────────────┘              └─────────────┘
   :3000                             :8000                          :5432
```

## Design Principles

1. **Separation of concerns** - The backend keeps HTTP, business logic, and persistence in distinct layers; domain errors are translated to HTTP codes at the edge. The frontend keeps API access (`lib/api`) separate from presentation (`components`).

2. **Configuration via environment variables** - No secrets or environment-specific values are hard-coded; everything flows through env vars and `.env`.

3. **Dependency safety** - The API rejects self-dependencies, cross-project dependencies, and any edge that would introduce a cycle.