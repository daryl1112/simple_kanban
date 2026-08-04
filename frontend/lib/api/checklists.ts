/** Checklist and checklist-item API calls. */

import type { Checklist, ChecklistItem } from "../types";
import { apiRequest } from "./client";

export function createChecklist(
  cardId: number,
  input: { title: string },
): Promise<Checklist> {
  return apiRequest<Checklist>(`/cards/${cardId}/checklists`, {
    method: "POST",
    json: input,
  });
}

export function renameChecklist(
  checklistId: number,
  input: { title: string },
): Promise<Checklist> {
  return apiRequest<Checklist>(`/checklists/${checklistId}`, {
    method: "PATCH",
    json: input,
  });
}

export function deleteChecklist(checklistId: number): Promise<void> {
  return apiRequest<void>(`/checklists/${checklistId}`, { method: "DELETE" });
}

export function addItem(
  checklistId: number,
  input: { text: string },
): Promise<ChecklistItem> {
  return apiRequest<ChecklistItem>(`/checklists/${checklistId}/items`, {
    method: "POST",
    json: input,
  });
}

/** Toggle completion and/or edit the text of an item. */
export function updateItem(
  itemId: number,
  input: Partial<{ text: string; is_completed: boolean }>,
): Promise<ChecklistItem> {
  return apiRequest<ChecklistItem>(`/checklist-items/${itemId}`, {
    method: "PATCH",
    json: input,
  });
}

export function deleteItem(itemId: number): Promise<void> {
  return apiRequest<void>(`/checklist-items/${itemId}`, { method: "DELETE" });
}
