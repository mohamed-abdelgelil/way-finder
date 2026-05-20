const API_BASE = "";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<string> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, message }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }

  const data = await res.json();
  return data.response as string;
}

export async function clearSession(sessionId: string): Promise<void> {
  await fetch(`${API_BASE}/session/${sessionId}`, { method: "DELETE" });
}
