/**
 * Thin fetch wrapper around the backend REST API.
 *
 * Centralises the base URL, JSON handling, and error normalisation so every
 * resource module (projects, cards, ...) shares identical request behaviour.
 */

/** Base URL of the backend, injected at build time; falls back to localhost. */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Error thrown for any non-2xx API response, carrying the status code. */
export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

/**
 * Perform a JSON request against the API.
 *
 * @param path   Path beginning with "/", e.g. "/projects".
 * @param options Standard fetch options; a JSON body may be passed as `json`.
 * @returns Parsed JSON, or `undefined` for 204 No Content responses.
 */
export async function apiRequest<T>(
  path: string,
  options: (RequestInit & { json?: unknown }) = {},
): Promise<T> {
  const { json, headers, ...rest } = options;
  const init: RequestInit = {
    ...rest,
    headers: {
      "Content-Type": "application/json",
      ...(headers ?? {}),
    },
  };
  if (json !== undefined) {
    init.body = JSON.stringify(json);
  }

  const response = await fetch(`${API_BASE}${path}`, init);

  if (!response.ok) {
    // Try to surface the backend's error detail; fall back to status text.
    let detail = response.statusText;
    try {
      const data = await response.json();
      if (data?.detail) detail = data.detail;
    } catch {
      /* response had no JSON body */
    }
    throw new ApiError(response.status, detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return (await response.json()) as T;
}
