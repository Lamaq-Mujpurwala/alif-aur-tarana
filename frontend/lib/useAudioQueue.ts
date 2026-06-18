"use client";

import { useCallback, useRef, useState } from "react";

/**
 * Plays base64 audio segments sequentially (cue, then reply) and exposes a live
 * amplitude `level` (0–1) + `speaking` flag to drive the chirāgh's glow.
 */
export function useAudioQueue() {
  const [level, setLevel] = useState(0);
  const [speaking, setSpeaking] = useState(false);
  const ctxRef = useRef<AudioContext | null>(null);
  const queueRef = useRef<string[]>([]);
  const playingRef = useRef(false);

  const playNext = useCallback(() => {
    const b64 = queueRef.current.shift();
    if (!b64) {
      playingRef.current = false;
      setSpeaking(false);
      setLevel(0);
      return;
    }
    playingRef.current = true;
    setSpeaking(true);

    const audio = new Audio("data:audio/mp3;base64," + b64);
    try {
      const ctx = ctxRef.current ?? (ctxRef.current = new AudioContext());
      if (ctx.state === "suspended") void ctx.resume();
      const source = ctx.createMediaElementSource(audio);
      const analyser = ctx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      analyser.connect(ctx.destination);
      const data = new Uint8Array(analyser.frequencyBinCount);
      const tick = () => {
        if (audio.paused || audio.ended) return;
        analyser.getByteFrequencyData(data);
        let sum = 0;
        for (const v of data) sum += v;
        setLevel(Math.min(1, (sum / data.length / 255) * 1.6));
        requestAnimationFrame(tick);
      };
      audio.addEventListener("play", tick, { once: true });
    } catch {
      /* WebAudio unavailable — audio still plays, just without amplitude */
    }
    audio.addEventListener("ended", playNext);
    audio.play().catch(playNext);
  }, []);

  const enqueue = useCallback(
    (b64?: string) => {
      if (!b64) return;
      queueRef.current.push(b64);
      if (!playingRef.current) playNext();
    },
    [playNext],
  );

  return { enqueue, level, speaking };
}
