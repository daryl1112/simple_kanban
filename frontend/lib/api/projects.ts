/** Project API calls. */

import type { Board, Project } from "../types";
import { apiRequest } from "./client";

export function listProjects(): Promise<Project[]> {
  return apiRequest<Project[]>("/projects");
}

export function getProject(id: number): Promise<Project> {
  return apiRequest<Project>(`/projects/${id}`);
}

export function createProject(input: {
  name: string;
  description?: string;
}): Promise<Project> {
  return apiRequest<Project>("/projects", { method: "POST", json: input });
}

export function updateProject(
  id: number,
  input: Partial<{ name: string; description: string }>,
): Promise<Project> {
  return apiRequest<Project>(`/projects/${id}`, { method: "PATCH", json: input });
}

export function deleteProject(id: number): Promise<void> {
  return apiRequest<void>(`/projects/${id}`, { method: "DELETE" });
}

export function getBoard(projectId: number): Promise<Board> {
  return apiRequest<Board>(`/projects/${projectId}/board`);
}
