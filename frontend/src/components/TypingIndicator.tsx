export function TypingIndicator() {
  return (
    <div style={{ display: "flex", alignItems: "center", marginBottom: 12 }}>
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
        }}
      >
        🏛️
      </div>
      <div
        style={{
          padding: "10px 16px",
          borderRadius: "18px 18px 18px 4px",
          background: "#ffffff",
          boxShadow: "0 1px 4px rgba(0,0,0,0.12)",
          display: "flex",
          gap: 5,
          alignItems: "center",
        }}
      >
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#c8a96e",
              display: "inline-block",
              animation: "bounce 1.2s infinite",
              animationDelay: `${i * 0.2}s`,
            }}
          />
        ))}
      </div>
    </div>
  );
}
