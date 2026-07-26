/** Card dependency API calls (server enforces acyclicity). */

import type { Card } from "../types";
import { apiRequest } from "./client";

export function addDependency(
  cardId: number,
  dependsOnId: number,
): Promise<Card> {
  return apiRequest<Card>(`/cards/${cardId}/dependencies`, {
    method: "POST",
    json: { depends_on_id: dependsOnId },
  });
}

export function removeDependency(
  cardId: number,
  dependsOnId: number,
): Promise<Card> {
  return apiRequest<Card>(`/cards/${cardId}/dependencies/${dependsOnId}`, {
    method: "DELETE",
  });
}
