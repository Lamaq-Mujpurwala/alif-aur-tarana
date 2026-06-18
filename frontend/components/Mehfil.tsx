"use client";

import { useCallback, useEffect, useState } from "react";
import type { Companion, ReplyTurn, ServerEvent } from "@/lib/types";
import { useAudioQueue } from "@/lib/useAudioQueue";
import { useConverse } from "@/lib/useConverse";
import { Chiragh } from "./Chiragh";
import { CompanionSwitch } from "./CompanionSwitch";
import { CueWhisper } from "./CueWhisper";
import { QalamInput } from "./QalamInput";
import { TriScript } from "./TriScript";

export default function Mehfil() {
  const [companion, setCompanion] = useState<Companion>("alif");
  const [you, setYou] = useState("");
  const [cue, setCue] = useState("");
  const [turn, setTurn] = useState<ReplyTurn | null>(null);
  const [status, setStatus] = useState("");
  const { enqueue, level, speaking } = useAudioQueue();

  // Re-tint the whole room to the active companion (CSS cross-fades --accent/--glow).
  useEffect(() => {
    document.body.className = `with-${companion}`;
  }, [companion]);

  const onEvent = useCallback(
    (e: ServerEvent) => {
      if (e.type === "transcript") setYou(e.text);
      else if (e.type === "cue") {
        setCue(e.text);
        enqueue(e.audio_b64);
      } else if (e.type === "reply") {
        setCue("");
        setTurn({ display: e.display, english_note: e.english_note });
        enqueue(e.audio_b64);
        setStatus(e.audio_b64 ? "" : "abhi aawaaz nahi aa paa rahi — alfaaz haazir hain");
      } else if (e.type === "error") {
        setStatus(e.message);
      }
    },
    [enqueue],
  );

  const { ready, sendText, sendAudio } = useConverse(onEvent);

  return (
    <main
      style={{
        minHeight: "100dvh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "32px 24px 40px",
      }}
    >
      <header style={{ display: "grid", justifyItems: "center", gap: 18, marginBottom: 8 }}>
        <div style={{ display: "grid", justifyItems: "center", gap: 2 }}>
          <span className="wordmark">الف اور ترانہ</span>
          <span className="label">Alif aur Tarana</span>
        </div>
        <CompanionSwitch companion={companion} onChange={setCompanion} />
      </header>

      <section
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          gap: 40,
          width: "100%",
          maxWidth: "var(--measure)",
          textAlign: "center",
        }}
      >
        <Chiragh level={level} speaking={speaking} />
        {turn ? <TriScript turn={turn} /> : <Welcome companion={companion} />}
      </section>

      <footer style={{ width: "100%", maxWidth: "var(--measure)", display: "grid", gap: 10 }}>
        {you ? (
          <p style={{ margin: 0, color: "var(--parchment-dim)", fontSize: "0.85rem", textAlign: "center" }}>
            Aap: {you}
          </p>
        ) : null}
        <CueWhisper text={cue} />
        <QalamInput
          onText={(t) => {
            setYou(t);
            sendText(companion, t);
          }}
          onAudio={(b64) => sendAudio(companion, b64)}
        />
        <p className="label" style={{ textAlign: "center", minHeight: 16 }}>
          {ready ? status : "raabta jod rahe hain…"}
        </p>
      </footer>
    </main>
  );
}

function Welcome({ companion }: { companion: Companion }) {
  return (
    <div style={{ display: "grid", gap: 16, maxWidth: "var(--measure)" }}>
      <p className="nastaliq" style={{ margin: 0, fontSize: "clamp(1.8rem, 4.5vw, 3rem)" }}>
        لفظ صرف معنی نہیں رکھتے… روشنی رکھتے ہیں
      </p>
      <p className="roman" style={{ margin: 0 }}>
        {companion === "alif"
          ? "Alif yahin hain. Kuch poochhiye — ya bas 'Alif suno' kehkar bulaaiye."
          : "Tarana yahin hain. Kuch poochhiye — ya bas 'Tarana suno' kehkar bulaaiye."}
      </p>
    </div>
  );
}
