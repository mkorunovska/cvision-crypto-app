import React from "react";

function RangeSelector({ range, onChange }) {
  if (!range) return null;

  return (
    <div style={{ marginTop: 20, marginBottom: 10 }}>
      <span style={{ marginRight: 8 }}>Range:</span>
      {["ALL", "365", "180", "90", "30"].map((r) => (
        <button
          key={r}
          onClick={() => onChange(r)}
          style={{
            marginRight: 8,
            padding: "6px 10px",
            borderRadius: 4,
            border: range === r ? "2px solid #808aa0ff" : "1px solid #9ca3af",
            background: range === r ? "#dbeafe" : "white",
            cursor: "pointer",
            color: "black",
          }}
        >
          {r === "ALL" ? "All" : `${r}d`}
        </button>
      ))}
    </div>
  );
}

export default RangeSelector;
