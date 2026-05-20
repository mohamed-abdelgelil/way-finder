import { useState, useCallback, useRef } from "react";
import { sendMessage, clearSession, ChatMessage } from "../api/chat";

function getOrCreateSessionId(): string {
  const key = "egypt_travel_session_id";
  let id = sessionStorage.getItem(key);
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem(key, id);
  }
  return id;
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const sessionId = useRef(getOrCreateSessionId());

  const send = useCallback(async (text: string) => {
    if (!text.trim() || isLoading) return;

    const userMsg: ChatMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    setError(null);

    try {
      const response = await sendMessage(sessionId.current, text);
      const assistantMsg: ChatMessage = { role: "assistant", content: response };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (e) {
      const msg = e instanceof Error ? e.message : "Something went wrong";
      setError(msg);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  const reset = useCallback(async () => {
    await clearSession(sessionId.current);
    // Generate a new session ID
    const newId = crypto.randomUUID();
    sessionStorage.setItem("egypt_travel_session_id", newId);
    sessionId.current = newId;
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isLoading, error, send, reset };
}
