import React from "react";

export default function AudioPlayback({ isSpeaking }) {
  return (
    <div
      aria-live="polite"
      style={{
        width: 72,
        height: 72,
        borderRadius: "50%",
        display: "grid",
        placeItems: "center",
        background: isSpeaking ? "#14532d" : "#1f2937",
        fontSize: "2rem",
      }}
    >
      🔊
    </div>
  );
}
