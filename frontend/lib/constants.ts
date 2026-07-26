/**
 * UI constants derived from the domain model: the ordered list of statuses and
 * their human labels / accent colors. Centralised so the board and card views
 * stay consistent.
 */

import type { CardStatus } from "./types";

/** Board columns in left-to-right order (matches the backend ordering). */
export const STATUS_ORDER: CardStatus[] = [
  "backlog",
  "approved",
  "in_progress",
  "review",
  "completed",
];

/** Human-readable label for each status. */
export const STATUS_LABELS: Record<CardStatus, string> = {
  backlog: "Backlog",
  approved: "Approved",
  in_progress: "In Progress",
  review: "Review",
  completed: "Completed",
};

/** Accent color per status, used for column headers and card chips. */
export const STATUS_COLORS: Record<CardStatus, string> = {
  backlog: "#64748b",
  approved: "#38bdf8",
  in_progress: "#f59e0b",
  review: "#a78bfa",
  completed: "#34d399",
};
