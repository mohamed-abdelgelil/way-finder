import { useChat } from "./hooks/useChat";
import { ChatWindow } from "./components/ChatWindow";
import { InputBar } from "./components/InputBar";

export default function App() {
  const { messages, isLoading, error, send, reset } = useChat();

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        flexDirection: "column",
        background: "#f5f0e8",
        fontFamily: "'Segoe UI', system-ui, sans-serif",
      }}
    >
      {/* Header */}
      <div
        style={{
          background: "linear-gradient(135deg, #8b6914, #c8a96e)",
          color: "#fff",
          padding: "14px 20px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 24 }}>🏛️</span>
          <div>
            <div style={{ fontWeight: 700, fontSize: 16 }}>Way-Finder</div>
            <div style={{ fontSize: 11, opacity: 0.85 }}>Egypt Travel Assistant</div>
          </div>
        </div>
        <button
          onClick={reset}
          title="Start new conversation"
          style={{
            background: "rgba(255,255,255,0.2)",
            border: "1px solid rgba(255,255,255,0.4)",
            color: "#fff",
            borderRadius: 8,
            padding: "5px 12px",
            fontSize: 12,
            cursor: "pointer",
          }}
        >
          New Chat
        </button>
      </div>

      {/* Error banner */}
      {error && (
        <div
          style={{
            background: "#fee2e2",
            color: "#991b1b",
            padding: "8px 16px",
            fontSize: 13,
            borderBottom: "1px solid #fca5a5",
            flexShrink: 0,
          }}
        >
          ⚠️ {error}
        </div>
      )}

      {/* Chat area */}
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        onSuggest={send}
      />

      {/* Input */}
      <InputBar onSend={send} disabled={isLoading} />
    </div>
  );
}
