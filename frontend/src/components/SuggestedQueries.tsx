const SUGGESTIONS = [
  "What destinations are available in Egypt?",
  "Find hotels in Cairo under $100 per night",
  "Plan a trip to Aswan with a budget of $200 for 2 nights",
  "What activities can I do in Hurghada for under $50?",
  "Tell me about Luxor",
  "What Egyptian restaurants are in Cairo?",
];

interface Props {
  onSelect: (query: string) => void;
}

export function SuggestedQueries({ onSelect }: Props) {
  return (
    <div style={{ padding: "0 16px 16px" }}>
      <p
        style={{
          fontSize: 12,
          color: "#888",
          marginBottom: 10,
          textAlign: "center",
        }}
      >
        Try asking...
      </p>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 8,
          justifyContent: "center",
        }}
      >
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => onSelect(s)}
            style={{
              padding: "6px 12px",
              borderRadius: 16,
              border: "1px solid #c8a96e",
              background: "transparent",
              color: "#8b6914",
              fontSize: 12,
              cursor: "pointer",
              transition: "all 0.15s",
            }}
            onMouseEnter={(e) => {
              (e.target as HTMLButtonElement).style.background = "#c8a96e";
              (e.target as HTMLButtonElement).style.color = "#fff";
            }}
            onMouseLeave={(e) => {
              (e.target as HTMLButtonElement).style.background = "transparent";
              (e.target as HTMLButtonElement).style.color = "#8b6914";
            }}
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
