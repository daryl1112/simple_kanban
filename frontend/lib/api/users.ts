/** User API calls (users exist so cards can be assigned). */

import type { User } from "../types";
import { apiRequest } from "./client";

export function listUsers(): Promise<User[]> {
  return apiRequest<User[]>("/users");
}

export function createUser(input: {
  name: string;
  email: string;
}): Promise<User> {
  return apiRequest<User>("/users", { method: "POST", json: input });
}
