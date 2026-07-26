/** Comment API calls (Markdown bodies). */

import type { Comment } from "../types";
import { apiRequest } from "./client";

export function listComments(cardId: number): Promise<Comment[]> {
  return apiRequest<Comment[]>(`/cards/${cardId}/comments`);
}

export function addComment(
  cardId: number,
  input: { body: string; author_id?: number | null },
): Promise<Comment> {
  return apiRequest<Comment>(`/cards/${cardId}/comments`, {
    method: "POST",
    json: input,
  });
}

export function deleteComment(commentId: number): Promise<void> {
  return apiRequest<void>(`/comments/${commentId}`, { method: "DELETE" });
}
