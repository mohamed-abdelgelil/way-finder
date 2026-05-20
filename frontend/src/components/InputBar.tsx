import { useState, KeyboardEvent } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export function InputBar({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        gap: 8,
        padding: "12px 16px",
        borderTop: "1px solid #e8e0d0",
        background: "#faf8f4",
      }}
    >
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about Egypt travel..."
        disabled={disabled}
        rows={1}
        style={{
          flex: 1,
          resize: "none",
          border: "1px solid #d4c5a0",
          borderRadius: 20,
          padding: "10px 16px",
          fontSize: 14,
          fontFamily: "inherit",
          outline: "none",
          background: disabled ? "#f0ece4" : "#fff",
          color: "#1a1a1a",
          lineHeight: 1.5,
          maxHeight: 120,
          overflowY: "auto",
          transition: "border-color 0.15s",
        }}
        onFocus={(e) => (e.target.style.borderColor = "#c8a96e")}
        onBlur={(e) => (e.target.style.borderColor = "#d4c5a0")}
      />
      <button
        onClick={handleSend}
        disabled={disabled || !value.trim()}
        style={{
          width: 40,
          height: 40,
          borderRadius: "50%",
          border: "none",
          background:
            disabled || !value.trim()
              ? "#d4c5a0"
              : "linear-gradient(135deg, #c8a96e, #8b6914)",
          color: "#fff",
          fontSize: 18,
          cursor: disabled || !value.trim() ? "not-allowed" : "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
          transition: "background 0.15s",
        }}
        aria-label="Send message"
      >
        ➤
      </button>
    </div>
  );
}
