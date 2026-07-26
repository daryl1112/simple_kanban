/**
 * Jest mock for react-markdown (which ships as ESM and would otherwise need
 * transforming). Renders the raw Markdown source so components under test can
 * still assert on their content. The real package is used in production.
 */
import type { ReactNode } from "react";

export default function ReactMarkdown({ children }: { children: ReactNode }) {
  return <div data-testid="markdown">{children}</div>;
}
