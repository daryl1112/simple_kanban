"use client";

import { useState } from "react";

import { projectsApi } from "@/lib/api";
import type { Project } from "@/lib/types";
import { Button } from "@/components/common";

interface CreateProjectFormProps {
  /** Called with the freshly created project so the parent can update state. */
  onCreated: (project: Project) => void;
}

/**
 * Controlled form for creating a project. Description accepts Markdown.
 * Note: no native <form> element — submission is wired via onClick per the
 * project's UI conventions.
 */
export function CreateProjectForm({ onCreated }: CreateProjectFormProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const project = await projectsApi.createProject({ name, description });
      onCreated(project);
      setName("");
      setDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create project");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="create-project">
      <input
        className="input"
        placeholder="New project name"
        aria-label="Project name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <textarea
        className="input"
        placeholder="Description (Markdown supported)"
        aria-label="Project description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      {error && <p className="error-text">{error}</p>}
      <Button onClick={handleSubmit} disabled={submitting}>
        {submitting ? "Creating…" : "Create project"}
      </Button>
    </div>
  );
}
