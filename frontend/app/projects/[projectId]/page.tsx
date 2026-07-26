"use client";

import { useEffect, useState } from "react";

import { projectsApi } from "@/lib/api";
import type { Project } from "@/lib/types";
import { Board } from "@/components/board";
import { Markdown } from "@/components/common";

/** Board page for a single project. */
export default function ProjectBoardPage({
  params,
}: {
  params: { projectId: string };
}) {
  const projectId = Number(params.projectId);
  const [project, setProject] = useState<Project | null>(null);

  useEffect(() => {
    projectsApi.getProject(projectId).then(setProject).catch(() => setProject(null));
  }, [projectId]);

  return (
    <div className="page page--board">
      <div className="page__head">
        <a href="/" className="link-btn">← Projects</a>
        <h1>{project ? project.name : `Project #${projectId}`}</h1>
      </div>
      {project?.description && (
        <div className="project-summary">
          <Markdown>{project.description}</Markdown>
        </div>
      )}
      <Board projectId={projectId} />
    </div>
  );
}
