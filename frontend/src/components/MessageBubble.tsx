import ReactMarkdown from "react-markdown";
import { ChatMessage } from "../api/chat";

interface Props {
  message: ChatMessage;
}

export function MessageBubble({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "12px",
      }}
    >
      {!isUser && (
        <div
          style={{
            width: 32,
            height: 32,
            borderRadius: "50%",
            background: "linear-gradient(135deg, #c8a96e, #8b6914)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 16,
            marginRight: 8,
            flexShrink: 0,
            alignSelf: "flex-end",
          }}
        >
          🏛️
        </div>
      )}
      <div
        style={{
          maxWidth: "72%",
          padding: "10px 14px",
          borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
          background: isUser
            ? "linear-gradient(135deg, #c8a96e, #8b6914)"
            : "#ffffff",
          color: isUser ? "#fff" : "#1a1a1a",
          boxShadow: "0 1px 4px rgba(0,0,0,0.12)",
          fontSize: 14,
          lineHeight: 1.6,
        }}
      >
        {isUser ? (
          <span>{message.content}</span>
        ) : (
          <ReactMarkdown
            components={{
              p: ({ children }) => (
                <p style={{ margin: "0 0 8px 0" }}>{children}</p>
              ),
              ul: ({ children }) => (
                <ul style={{ margin: "4px 0", paddingLeft: 20 }}>{children}</ul>
              ),
              li: ({ children }) => (
                <li style={{ marginBottom: 4 }}>{children}</li>
              ),
              strong: ({ children }) => (
                <strong style={{ color: "#8b6914" }}>{children}</strong>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
}
