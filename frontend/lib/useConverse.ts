"use client";

import { useEffect, useRef, useState } from "react";
import type { Companion, ServerEvent } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";

/** Opens the /converse WebSocket and forwards server events to `onEvent`. */
export function useConverse(onEvent: (e: ServerEvent) => void) {
  const wsRef = useRef<WebSocket | null>(null);
  const handlerRef = useRef(onEvent);
  handlerRef.current = onEvent;
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const url = API_BASE.replace(/^http/, "ws") + "/converse";
    const ws = new WebSocket(url);
    wsRef.current = ws;
    ws.onopen = () => setReady(true);
    ws.onclose = () => setReady(false);
    ws.onerror = () => setReady(false);
    ws.onmessage = (ev) => {
      try {
        handlerRef.current(JSON.parse(ev.data) as ServerEvent);
      } catch {
        /* ignore malformed frames */
      }
    };
    return () => ws.close();
  }, []);

  const send = (payload: object) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) ws.send(JSON.stringify(payload));
  };

  return {
    ready,
    sendText: (companion: Companion, text: string) => send({ type: "text", companion, text }),
    sendAudio: (companion: Companion, audio_b64: string) =>
      send({ type: "audio", companion, audio_b64 }),
  };
}
