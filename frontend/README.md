# DevBoard UI (frontend)

Next.js (App Router, TypeScript) client for the DevBoard Kanban tool. It talks
to the backend REST API; every action here has an API equivalent.

## Structure

```
app/                         # routes (App Router)
├── page.tsx                 # projects landing
├── projects/[projectId]/    # board view
└── layout.tsx, globals.css  # shell + styles
components/
├── board/                   # Board, Column, CardItem, CardModal
├── projects/                # ProjectList, CreateProjectForm
└── common/                  # Button, Modal, Markdown
lib/
├── api/                     # one module per resource + fetch client
├── types.ts                 # domain types mirroring the API
└── constants.ts             # status order, labels, colors
__tests__/                   # jest + React Testing Library
```

## Configuration

`NEXT_PUBLIC_API_URL` — base URL the browser uses to reach the backend
(default `http://localhost:8000`). See `.env.example`.

## Running locally

```bash
npm install
npm run dev        # http://localhost:3000
```

## Tests

```bash
npm test
```

react-markdown / remark-gfm are ESM-only; in tests they are mapped to
lightweight mocks (`__mocks__/`) so the suite runs without transforming their
ESM dependency trees. The real packages are used at build and runtime.

## Board interactions

- Drag a card between columns to change its status (native HTML5 drag-and-drop).
- Click a card to open its editor: title, Markdown description (with preview),
  status, assignee, dependencies, checklists, and Markdown comments.
- Add checklists of checkable items; each shows a progress bar, and the card
  displays an aggregate progress badge on the board.
