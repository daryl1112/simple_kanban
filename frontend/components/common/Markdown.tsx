"use client";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface MarkdownProps {
  /** Raw Markdown source (from a card description or comment body). */
  children: string;
}

/**
 * Render Markdown as safe HTML. GitHub-Flavored Markdown (tables, task lists,
 * strikethrough) is enabled via remark-gfm. react-markdown does not render raw
 * HTML by default, so this is safe against HTML injection.
 */
export function Markdown({ children }: MarkdownProps) {
  return (
    <div className="markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children}</ReactMarkdown>
    </div>
  );
}
