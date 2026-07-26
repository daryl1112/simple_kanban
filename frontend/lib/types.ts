/**
 * Shared domain types mirroring the backend's API schemas.
 * Kept in one place so components and API modules agree on shapes.
 */

/** The five board columns, matching the backend `CardStatus` enum. */
export type CardStatus =
  | "backlog"
  | "approved"
  | "in_progress"
  | "review"
  | "completed";

export interface Project {
  id: number;
  name: string;
  /** Markdown source. */
  description: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
}

export interface Comment {
  id: number;
  card_id: number;
  author_id: number | null;
  /** Markdown source. */
  body: string;
  created_at: string;
  updated_at: string;
}

export interface Card {
  id: number;
  project_id: number;
  title: string;
  /** Markdown source. */
  description: string;
  status: CardStatus;
  assignee_id: number | null;
  dependency_ids: number[];
  comments: Comment[];
  created_at: string;
  updated_at: string;
}

export interface BoardColumn {
  status: CardStatus;
  cards: Card[];
}

export interface Board {
  project_id: number;
  columns: BoardColumn[];
}
