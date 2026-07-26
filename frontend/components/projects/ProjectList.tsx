"use client";

import Link from "next/link";

import type { Project } from "@/lib/types";
import { Markdown } from "@/components/common";

interface ProjectListProps {
  projects: Project[];
}

/** Grid of project cards, each linking to its board. */
export function ProjectList({ projects }: ProjectListProps) {
  if (projects.length === 0) {
    return <p className="empty-state">No projects yet. Create your first one to get started.</p>;
  }

  return (
    <ul className="project-list">
      {projects.map((project) => (
        <li key={project.id} className="project-card">
          <Link href={`/projects/${project.id}`} className="project-card__link">
            <span className="mono id-badge">#{project.id}</span>
            <h3>{project.name}</h3>
          </Link>
          {project.description && (
            <div className="project-card__desc">
              <Markdown>{project.description}</Markdown>
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
