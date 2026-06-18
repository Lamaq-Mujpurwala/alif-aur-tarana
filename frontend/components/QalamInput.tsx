"use client";

import { useRef, useState } from "react";

/** The qalam — one quiet line: type, or hold the feather to speak. */
export function QalamInput({
  onText,
  onAudio,
}: {
  onText: (text: string) => void;
  onAudio: (audioB64: string) => void;
}) {
  const [value, setValue] = useState("");
  const [recording, setRecording] = useState(false);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const submit = () => {
    const text = value.trim();
    if (!text) return;
    onText(text);
    setValue("");
  };

  const toggleMic = async () => {
    if (recorderRef.current?.state === "recording") {
      recorderRef.current.stop();
      return;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mr = new MediaRecorder(stream);
      recorderRef.current = mr;
      chunksRef.current = [];
      mr.ondataavailable = (e) => chunksRef.current.push(e.data);
      mr.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        setRecording(false);
        const blob = new Blob(chunksRef.current, { type: mr.mimeType || "audio/webm" });
        onAudio(await blobToB64(blob));
      };
      mr.start();
      setRecording(true);
    } catch {
      setRecording(false);
    }
  };

  return (
    <div className="qalam">
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") submit();
        }}
        placeholder='kahiye… ya "Alif suno" keh kar bulaaiye'
        aria-label="message"
      />
      <button
        className="btn-icon btn-mic"
        data-rec={recording}
        onClick={toggleMic}
        aria-label={recording ? "stop recording" : "speak"}
        title="bol kar baat kijiye"
      >
        {recording ? "■" : "🪶"}
      </button>
      <button className="btn-icon btn-send" onClick={submit} aria-label="send" title="bhejiye">
        ▸
      </button>
    </div>
  );
}

const blobToB64 = (blob: Blob) =>
  new Promise<string>((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(String(reader.result).split(",")[1]);
    reader.readAsDataURL(blob);
  });
