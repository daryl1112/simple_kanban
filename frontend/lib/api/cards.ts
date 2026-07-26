/** Card API calls: create, edit, move, assign, delete. */

import type { Card, CardStatus } from "../types";
import { apiRequest } from "./client";

export function createCard(
  projectId: number,
  input: {
    title: string;
    description?: string;
    status?: CardStatus;
    assignee_id?: number | null;
  },
): Promise<Card> {
  return apiRequest<Card>(`/projects/${projectId}/cards`, {
    method: "POST",
    json: input,
  });
}

export function getCard(cardId: number): Promise<Card> {
  return apiRequest<Card>(`/cards/${cardId}`);
}

/**
 * Partially update a card. Also the single way to move a card between columns
 * (pass `status`) or (un)assign it (pass `assignee_id`, `null` to clear).
 */
export function updateCard(
  cardId: number,
  input: Partial<{
    title: string;
    description: string;
    status: CardStatus;
    assignee_id: number | null;
  }>,
): Promise<Card> {
  return apiRequest<Card>(`/cards/${cardId}`, { method: "PATCH", json: input });
}

export function deleteCard(cardId: number): Promise<void> {
  return apiRequest<void>(`/cards/${cardId}`, { method: "DELETE" });
}
