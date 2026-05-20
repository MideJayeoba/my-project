import React from "react";

export default function VoiceCapture({ isRecording, onToggle }) {
  return (
    <button
      type="button"
      onClick={onToggle}
      aria-label={isRecording ? "Stop recording" : "Start recording"}
      style={{
        width: 88,
        height: 88,
        borderRadius: "50%",
        border: "2px solid #7dd3fc",
        background: isRecording ? "#7f1d1d" : "#0f172a",
        color: "#f8fafc",
        fontSize: "2rem",
        cursor: "pointer",
      }}
    >
      🎤
    </button>
  );
}
