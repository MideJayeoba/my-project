import React from "react";

const STATUS_ICON = {
  idle: "🫧",
  listening: "🎙️",
  processing: "〰️",
  speaking: "📢",
  error: "⚠️",
};

export default function StatusIndicator({ status }) {
  return (
    <div
      style={{
        width: 120,
        height: 120,
        borderRadius: "50%",
        border: "3px solid #38bdf8",
        display: "grid",
        placeItems: "center",
        fontSize: "3rem",
        animation: status !== "idle" ? "pulse 1.3s infinite" : "none",
      }}
      role="img"
      aria-label={status}
    >
      {STATUS_ICON[status] ?? STATUS_ICON.idle}
    </div>
  );
}
