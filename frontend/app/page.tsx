"use client";

import { useEffect, useState } from "react";

import { projectsApi } from "@/lib/api";
import type { Project } from "@/lib/types";
import { CreateProjectForm, ProjectList } from "@/components/projects";

/** Landing page: list existing projects and create new ones. */
export default function HomePage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    projectsApi
      .listProjects()
      .then(setProjects)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load projects"),
      );
  }, []);

  return (
    <div className="page">
      <div className="page__head">
        <h1>Projects</h1>
      </div>
      {error && <p className="error-text">{error}</p>}
      <CreateProjectForm onCreated={(p) => setProjects((prev) => [...prev, p])} />
      <ProjectList projects={projects} />
    </div>
  );
}
