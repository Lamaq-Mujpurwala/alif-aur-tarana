# Alif Aur Tarana — Frontend (Next.js)

The voice-first companion UI, realising the **Shab-e-Mehfil** design system
([`../design/DESIGN.md`](../design/DESIGN.md)). Next.js (App Router) + TypeScript +
Tailwind v4 + Framer Motion.

## Run

```bash
# 1) start the backend first (from ../backend): uv run uvicorn aat.main:app --reload  -> :8000
# 2) then, here:
npm install         # if not already
npm run dev         # -> http://localhost:3000
```

By default it talks to the backend at `http://localhost:8000` (the `/converse` WebSocket).
Override with `NEXT_PUBLIC_API_BASE` in `.env.local` (see `.env.local.example`).

## Structure
```
app/
  layout.tsx     # fonts (Gulzar + Noto Nastaliq + Tiro Devanagari) on <html>, theme class on <body>
  globals.css    # the Shab-e-Mehfil tokens (ported from ../design/tokens.css) + components
  page.tsx       # renders <Mehfil/>
components/
  Mehfil.tsx         # orchestrator: state + /converse stream + layout
  Chiragh.tsx        # the breathing, voice-reactive lamp (companion presence)
  TriScript.tsx      # Nastaʿlīq hero (ink-settle reveal) + Roman + Devanagari + note
  CompanionSwitch.tsx# Alif (ا) / Tarana (◐) sigils — re-tints the room
  QalamInput.tsx     # type or speak (mic)
  CueWhisper.tsx     # the acknowledgement cue, whispered above the input
lib/
  useConverse.ts     # /converse WebSocket hook
  useAudioQueue.ts   # sequential audio (cue -> reply) + amplitude for the chirāgh
  types.ts
```

## Type / motion notes
- Latin display (Zodiak) + body (Switzer) load from **Fontshare** via `@import` in `globals.css`.
- Companion theming: `<body class="with-alif|with-tarana">` swaps `--accent`/`--glow`; the
  registered `@property` colours cross-fade over `--dur-3`.
- Components to source/re-skin later (Framer Marketplace via `unframer`, or 21st.dev): a richer
  background and an ink-reveal — see `../design/DESIGN.md §12`.
