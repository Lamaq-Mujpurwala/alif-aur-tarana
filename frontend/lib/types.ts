export type Companion = "alif" | "tarana";

export interface TriScript {
  urdu: string;
  roman: string;
  devanagari: string;
}

export interface ReplyTurn {
  display: TriScript;
  english_note?: string;
}

/** Events streamed from the backend /converse WebSocket. */
export type ServerEvent =
  | { type: "transcript"; text: string }
  | { type: "cue"; role: string; text: string; audio_b64: string }
  | { type: "reply"; display: TriScript; english_note?: string; audio_b64: string }
  | { type: "error"; message: string };
