import { useCallback, useRef, useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function useVoicePipeline() {
  const [status, setStatus] = useState("idle");
  const [isRecording, setIsRecording] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const processAudioBlob = useCallback(async (audioBlob) => {
    setStatus("processing");

    const formData = new FormData();
    formData.append("file", audioBlob, "recording.webm");

    const transcribeRes = await fetch(`${API_BASE}/transcribe`, {
      method: "POST",
      body: formData,
    });
    if (!transcribeRes.ok) throw new Error("transcribe failed");
    const { transcript } = await transcribeRes.json();

    const reasonRes = await fetch(`${API_BASE}/reason`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript }),
    });
    if (!reasonRes.ok) throw new Error("reason failed");
    const { guidance } = await reasonRes.json();

    const speakRes = await fetch(`${API_BASE}/speak`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: guidance }),
    });
    if (!speakRes.ok) throw new Error("speak failed");

    const audioBlobOut = await speakRes.blob();
    const audioUrl = URL.createObjectURL(audioBlobOut);
    const audio = new Audio(audioUrl);
    setIsSpeaking(true);
    setStatus("speaking");

    await new Promise((resolve, reject) => {
      audio.onended = resolve;
      audio.onerror = reject;
      audio.play().catch(reject);
    });

    URL.revokeObjectURL(audioUrl);
    setIsSpeaking(false);
    setStatus("idle");
  }, []);

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    setIsRecording(false);
  }, []);

  const startRecording = useCallback(async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    chunksRef.current = [];

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) chunksRef.current.push(event.data);
    };

    recorder.onstop = async () => {
      try {
        const blob = new Blob(chunksRef.current, { type: "audio/webm" });
        await processAudioBlob(blob);
      } catch {
        setStatus("error");
      } finally {
        stream.getTracks().forEach((t) => t.stop());
      }
    };

    recorder.start();
    mediaRecorderRef.current = recorder;
    setStatus("listening");
    setIsRecording(true);
  }, [processAudioBlob]);

  const toggleRecording = useCallback(async () => {
    if (isRecording) {
      stopRecording();
      return;
    }
    try {
      await startRecording();
    } catch {
      setStatus("error");
    }
  }, [isRecording, startRecording, stopRecording]);


  return { status, isRecording, isSpeaking, toggleRecording };
}
