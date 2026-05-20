import { useEffect, useRef } from "react";
import { ChatMessage } from "../api/chat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { SuggestedQueries } from "./SuggestedQueries";

interface Props {
  messages: ChatMessage[];
  isLoading: boolean;
  onSuggest: (query: string) => void;
}

export function ChatWindow({ messages, isLoading, onSuggest }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const isEmpty = messages.length === 0 && !isLoading;

  return (
    <div
      style={{
        flex: 1,
        overflowY: "auto",
        padding: "16px 16px 0",
        display: "flex",
        flexDirection: "column",
      }}
    >
      {isEmpty ? (
        <div
          style={{
            flex: 1,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            gap: 16,
            color: "#888",
          }}
        >
          <div style={{ fontSize: 48 }}>🇪🇬</div>
          <div style={{ textAlign: "center" }}>
            <p style={{ fontSize: 18, fontWeight: 600, color: "#5a4a2a", margin: 0 }}>
              Egypt Travel Assistant
            </p>
            <p style={{ fontSize: 13, marginTop: 6 }}>
              Ask me about destinations, hotels, restaurants, activities, or let me plan your whole trip.
            </p>
          </div>
          <SuggestedQueries onSelect={onSuggest} />
        </div>
      ) : (
        <>
          {messages.map((msg, i) => (
            <MessageBubble key={i} message={msg} />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={bottomRef} />
        </>
      )}
    </div>
  );
}
