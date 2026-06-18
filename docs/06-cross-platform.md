# 06 · Cross-Platform Strategy

You want this everywhere you consume Urdu content: the web, your phone, **a YouTube extension**, and ideally hooking into **YouTube Music on the phone**. This doc lays out a realistic, phased multi-surface plan and is honest about what each platform allows.

> **Guiding principle:** one **backend brain** (the FastAPI + Pipecat agent from [`03`](03-architecture.md)), many **thin clients**. Every surface is just a different way to (a) capture your voice/the content you're consuming and (b) talk to the same companions. Build the brain once; add surfaces over time.

---

## 1. Surface map (and the order to build them)

| Phase | Surface | Effort | Why this order |
|-------|---------|--------|----------------|
| 1 | **Web app (Next.js PWA)** | Low | Fastest path to a *talking companion*; works on desktop + mobile browsers; installable |
| 2 | **PWA polish → "installed app" feel on phone** | Low | Add-to-home-screen, mic permissions, background audio, offline shell |
| 3 | **Browser extension (YouTube)** | Medium | Learn-while-watching on desktop; reuses the same backend |
| 4 | **Native mobile app (Expo/React Native)** | Medium-High | True background audio, share-sheet, OS integration |
| 5 | **YouTube Music on phone integration** | High / constrained | The hardest; needs the native app + OS hooks (see §5) |

---

## 2. Web app (PWA) — the home base

**Stack:** Next.js (App Router) + TypeScript + Tailwind, talking to the FastAPI backend over WebSocket.

- **Voice in/out in the browser:** `getUserMedia` for mic, Web Audio API for playback, WebSocket (MVP) or WebRTC (later) to stream audio. Pipecat has a JS/React client SDK that pairs with the Python backend.
- **PWA = installable everywhere:** a manifest + service worker makes it add-to-home-screen on Android/iOS and desktop, with an app-like full-screen shell, splash, and offline shell. **One codebase covers web + a credible "mobile app" for the MVP** without app-store friction.
- **The companion UI:** an animated orb/character that reacts to speech amplitude; the **tri-script transcript** (Nastaʿlīq / Devanagari / Roman) with tap-to-hear; a minimal, calm, content-first layout ([`01 §6`](01-product-vision.md), inspiration in [`inspiration/`](inspiration/)).
- **PWA limits to know:** iOS Safari restricts background audio and some mic behaviours; true always-listening background is a native-app feature (Phase 4). For MVP, **push-to-talk or tap-to-start** is fine and even nicer for a learning tool.

> **Phase 1 deliverable:** open the web app, pick Alif/Tarana, talk, get a beautifully-voiced, tri-script reply. That alone validates the whole product.

---

## 3. Mobile app (Phase 4) — Expo / React Native

When the PWA's limits bite (background listening, richer OS integration, app-store presence):

- **Expo (React Native)** reuses your TS skills and the `packages/shared-types` event protocol; one codebase → iOS + Android.
- Native wins it unlocks: **background audio sessions**, lock-screen/media controls, **share-sheet target** ("share this YouTube/Spotify link to Alif Aur Tarana"), push notifications ("aaj ka sher tayyar hai"), and the OS hooks needed for §5.
- Alternative: keep PWA and wrap with **Capacitor** if you want app-store presence with minimal rewrite. Expo is the better long-term native bet.

---

## 4. Browser extension (Phase 3) — learn while you watch YouTube

This is the first "meet the content where it lives" surface, and it's very achievable on **desktop**.

**Tech:** Manifest V3 extension via **WXT** (modern DX, TS, HMR) or plain MV3. Chrome + Firefox + Edge.

**What it does:**
- A **content script** on `youtube.com` detects the current video (ID, title) and grabs the transcript (via the backend's `youtube.transcript` tool, [`04`](04-tools-and-integrations.md)).
- A small **overlay companion** (side panel or floating orb) lets you say *"Tarana, is line ka matlab?"* about whatever's playing; it can read the **current caption line** as you watch.
- **"Explain this line" hotkey / button** on the player; pause → companion unpacks the lyric/dialogue tri-script.
- Talks to the **same FastAPI backend** — the extension is just another thin client.

**Constraints (be realistic):**
- MV3 background is a service worker (ephemeral); keep state in the backend, not the worker.
- Mic capture in an extension is doable but permission-fiddly; the side-panel page can host the audio session.
- YouTube DOM changes; rely on the backend transcript tool + the official caption track rather than scraping the DOM where possible.

> **Phase 3 deliverable:** watching a ghazal/film song on YouTube, hit "explain", and a companion teaches you the line you just heard — same voice, same memory, same tri-script.

---

## 5. YouTube Music on the phone — the hard one (honest assessment)

You specifically want to hook into **YouTube Music on the phone**. This is the **most constrained** surface, so here's the unvarnished reality and the workable paths.

**Why it's hard:** browser extensions **don't exist on mobile YouTube Music** (it's a native app, not a web page you can inject into). Mobile OSes sandbox apps; you can't "read another app's screen" without special, heavy permissions. So we can't drop an overlay into YT Music the way the desktop extension drops into youtube.com.

**The realistic paths (best → most invasive):**

| Path | How it works | Effort | UX | Caveats |
|------|--------------|--------|-----|---------|
| **A. Share-sheet** ✅ recommended | In YT Music/YouTube, tap Share → "Alif Aur Tarana" → our app receives the track link → fetches transcript → teaches it | Medium (needs native app, Phase 4) | One tap from any music/video app | Manual per-song, but dead simple & reliable |
| **B. Now-Playing via Notification/Media listener (Android)** | Android `NotificationListenerService` / `MediaSessionManager` reads the *currently playing* track metadata (title/artist) the system already exposes | High | "Magic": app knows what you're listening to, offers to explain it | Android-only; needs sensitive notification-access permission; reads metadata, **not** lyrics (we still fetch lyrics via our YouTube tool) |
| **C. System-wide floating overlay (Android)** | A draggable companion bubble (`SYSTEM_ALERT_WINDOW`) floats over YT Music; tap to ask about the current track (combined with B for context) | High | Closest to "always-there friend" | Android-only; overlay permission; battery/UX care |
| **D. Manual paste / voice** | "Alif, abhi main 'Tum Aaye' sun raha hoon" or paste a link | Low | Works today, any platform | Not automatic |
| **E. (iOS) Shortcuts + Share** | iOS Shortcuts share extension; "Share to Alif Aur Tarana" | Medium | Good on iOS where B/C are impossible | iOS sandbox forbids B/C entirely |

**Recommendation:** Ship **D (manual/voice)** in the PWA now (zero new tech), then **A (share-sheet)** with the Phase-4 native app (covers *every* music/video app, both OSes, reliably). Treat **B+C (Android now-playing + floating bubble)** as a delightful **Android-only "power mode"** later — it's the "wow", but it needs sensitive permissions and Android-specific work. **iOS** will never allow B/C, so A/E is the iOS ceiling — design for that.

> Key insight: we don't need to *read* YT Music's audio. We need the **track identity** (title/artist), then our own YouTube/web tools fetch the lyrics/meaning. Paths A/B just automate "which song is this?". That keeps the integration light and legal.

**Spotify note:** Spotify *does* have an official Web API (now-playing, track metadata) and lyrics partners — if your listening is on Spotify too, that's an *easier* automatic hook than YT Music. Worth supporting alongside (a "connect Spotify" button → companion knows your current track). YT Music's API is far less open, which is exactly why share-sheet is the pragmatic YT Music answer.

---

## 6. One brain, many clients — the shared contract

All surfaces speak the same small WebSocket event protocol ([`03 §6.4`](03-architecture.md)), and share:
- the **same companions & memory** (talk on desktop, continue on phone — Alif remembers),
- the **same tools** (Rekhta/YouTube/web),
- the **same `packages/shared-types`** so web/extension/mobile stay in sync.

```
        Web PWA ─┐
   YT Extension ─┤
   Mobile (Expo) ─┼──WebSocket(events)──►  FastAPI + Pipecat brain  ──►  Gemini/Sarvam/ElevenLabs/Azure
 Share-sheet/now-playing ─┘                 (personas · tools · memory)
```

---

## 7. Phase-by-phase platform deliverables

| Phase | Ship |
|-------|------|
| 1 | Web PWA: talk to Alif/Tarana, tri-script replies (push-to-talk) |
| 2 | PWA installable on phone; smoother streaming; basic memory across sessions |
| 3 | Chrome/Firefox **YouTube extension**: "explain this line" while watching |
| 4 | **Expo native app**: background audio, **share-sheet** ("share song → companion") |
| 5 | **Android power mode**: now-playing detection + floating bubble over YT Music; Spotify connect |

Next: the full execution roadmap, free-tier budget and risks → [`07-execution-roadmap.md`](07-execution-roadmap.md).

---

### Notes & sources
- PWA installability/limits and Expo/Capacitor are standard platform capabilities (MDN PWA docs; Expo docs) — no controversial claims here.
- Android **NotificationListenerService / MediaSessionManager** expose active media metadata to permitted apps; **SYSTEM_ALERT_WINDOW** enables overlays — both standard Android APIs with sensitive-permission gates (Android developer docs).
- iOS sandbox prohibits reading other apps' state; Share Extensions / Shortcuts are the sanctioned cross-app path (Apple developer docs).
- YouTube transcript access for the extension reuses the tools in [`04-tools-and-integrations.md`](04-tools-and-integrations.md): [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api).
- Pipecat client SDKs (web/React) pair with the Python backend: [Pipecat vs LiveKit](https://www.f22labs.com/blogs/difference-between-livekit-vs-pipecat-voice-ai-platforms/).
