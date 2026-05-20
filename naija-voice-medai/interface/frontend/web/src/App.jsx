import React from "react";
import VoiceCapture from "./VoiceCapture";
import AudioPlayback from "./AudioPlayback";
import StatusIndicator from "./StatusIndicator";
import useVoicePipeline from "./hooks/useVoicePipeline";

export default function App() {
  const { status, isRecording, isSpeaking, toggleRecording } = useVoicePipeline();

  return (
    <main
      style={{
        minHeight: "100vh",
        margin: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "radial-gradient(circle at center, #0f172a, #020617)",
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1.5rem",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <StatusIndicator status={status} />
        <VoiceCapture isRecording={isRecording} onToggle={toggleRecording} />
        <AudioPlayback isSpeaking={isSpeaking} />
      </div>
    </main>
  );
}
