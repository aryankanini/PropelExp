const BACKEND_ORIGIN = import.meta.env.VITE_BACKEND_ORIGIN ?? "https://propelexp.onrender.com/";

export function apiUrl(path: string): string {
  return `${BACKEND_ORIGIN}${path}`;
}

export function sessionHeaders(sessionId: string): Record<string, string> {
  return { "X-Session-ID": sessionId };
}

export async function apiFetch(
  path: string,
  sessionId: string,
  init?: RequestInit,
): Promise<Response> {
  return fetch(apiUrl(path), {
    ...init,
    headers: {
      ...sessionHeaders(sessionId),
      ...(init?.headers ?? {}),
    },
  });
}
